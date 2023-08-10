#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import urllib.request
from typing import List

CIRRUS_API = "https://api.cirrus-ci.com/graphql"

QUERY = """
query ($platform: String!, $owner: String!, $repo: String!, $tag: String!) {
  ownerRepository(platform: $platform, owner: $owner, name: $repo) {
    builds(branch: $tag) {
      edges {
         node {
          id,
          tag,
          senderUserPermissions,
          status,
          changeIdInRepo
        }
      }
    }
  }
}
"""


def find(owner: str, repo: str, tag: str, commit: str) -> str:
    body = {
        "query": QUERY,
        "variables": {
            "platform": "github",
            "owner": owner,
            "repo": repo,
            "tag": tag,
        },
    }
    with urllib.request.urlopen(CIRRUS_API, json.dumps(body).encode()) as r:
        response = json.loads(r.read())

    nodes: List[dict[str, str]] = []
    for edge in response["data"]["ownerRepository"]["builds"]["edges"]:
        nodes.append(edge["node"])

    if len(nodes) == 0:
        raise ValueError(f"no builds found for {owner}/{repo}@{tag}")

    filtered = list(filter(lambda c: c["changeIdInRepo"] == commit, nodes))
    if len(filtered) == 0:
        raise ValueError(f"no builds matched commit {commit}")
    elif len(filtered) > 1:
        raise ValueError(f"multiple builds matched commit {commit}")

    build = filtered[0]
    if (q := build["tag"]) != tag:
        raise ValueError(f"build has tag {q}, expected {tag}")
    if (q := build["senderUserPermissions"]) != "admin":
        raise ValueError(f"build initiated by {q}, not admin")
    if (q := build["status"]) != "COMPLETED":
        raise ValueError(f"build in {q}, not COMPLETED")

    return build["id"]


if __name__ == "__main__":
    sys.tracebacklimit = 0

    if len(sys.argv) != 4:
        print(f"usage: {sys.argv[0]} OWNER/REPO TAG COMMIT")
        sys.exit(1)
    _, full, tag, commit = sys.argv
    owner, repo = full.split("/")

    build = find(owner, repo, tag, commit)
    print(build)
