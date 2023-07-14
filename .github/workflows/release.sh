#!/bin/bash

set -eux -o pipefail
shopt -s failglob

# Find the latest (annotated) tag and check that it's well-formed
export RELEASE_TAG=$(git describe --abbrev=0)
if [[ ! "$(git show $RELEASE_TAG)" =~ "tmpdir@$RELEASE_TAG" ]]; then
    echo "error: tag is missing repository and version"
    exit 1
fi

curl https://github.com/btidor.gpg | gpg --import
git verify-tag "$RELEASE_TAG"

# Query Cirrus CI to find the build that was triggered by this tag being
# created. Note that the build triggered by the corresponding commit will *not*
# work since those artifacts don't contain the correct version number.
export BUILD_QUERY='
query ($platform: String!, $owner: String!, $repo: String!, $tag: String!) {
  ownerRepository(platform: $platform, owner: $owner, name: $repo) {
    builds(branch: $tag) {
      edges {
         node {
          id,
          tag,
          senderUserPermissions,
          status
        }
      }
    }
  }
}'

export RESPONSE=$(curl https://api.cirrus-ci.com/graphql --data @- <<EOF
{
    "query": "$BUILD_QUERY",
    "variables": {
        "platform": "github",
        "owner": "btidor",
        "repo": "tmpdir",
        "tag": "$RELEASE_TAG"
    }
}
EOF
)

# Validate the response from Cirrus CI
export EDGES="$(jq -en 'env.RESPONSE|fromjson.data.ownerRepository.builds.edges')"
if [ "$(jq -en 'env.EDGES|fromjson|length')" != "1" ]; then
    echo "error: multiple builds found for $RELEASE_TAG"
    exit 1
fi

export BUILD="$(jq -en 'env.EDGES|fromjson[0].node')"
if [ "$(jq -enr 'env.BUILD|fromjson.tag')" != "$RELEASE_TAG" ]; then
    echo "error: tag did not match $RELEASE_TAG"
    exit 1
fi

if [ "$(jq -enr 'env.BUILD|fromjson.senderUserPermissions')" != "admin" ]; then
    echo "error: build not initiated by an admin"
    exit 1
fi

if [ "$(jq -enr 'env.BUILD|fromjson.status')" != "COMPLETED" ]; then
    echo "error: build not in COMPLETED"
    exit 1
fi

export BUILD_ID="$(jq -enr 'env.BUILD|fromjson.id')"

# Download the build artifacts from Cirrus CI and upload them to the GitHub
# release, then publish it.
curl --output wheels.zip "https://api.cirrus-ci.com/v1/artifact/build/$BUILD_ID/wheels.zip"
unzip wheels.zip
gh release upload "$RELEASE_TAG" wheelhouse/*
gh release edit "$RELEASE_TAG" --draft=false
