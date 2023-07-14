DEPDIR = /opt
INCLUDE = /usr/local/include
REVISION = 1230d80a5275ddf525da9c218c2bcd29c3130e49

.PHONY: all build clean ci docs release

all: build

build: clean
	python3 -m build

docs:
	make -C docs clean
	ZBITVECTOR_SOLVER=dummy O=-W make -C docs html
	python3 -m http.server --directory docs/_build/html/

release:
	@bash -c '[[ "$V" =~ ^[0-9]+\.[0-9]+\.[0-9]+$$ ]] || \
		(echo "usage: make release V=x.y.z"; exit 1)'
	git tag -s "v$V" -m "tmpdir@v$V"
	git push tmpdir "v$V"
	@echo "\n1. Draft release:\n   https://github.com/btidor/tmpdir/releases/tag/v$V"
	@echo "\n2. Wait for build:\n   https://cirrus-ci.com/github/btidor/tmpdir/v$V"
	@echo "\n3. Check artifacts:\n   https://api.cirrus-ci.com/v1/artifact/build/NNNNNN/wheels.zip"
	@echo "\n4. Finalize release:\n   https://github.com/btidor/tmpdir/actions/workflows/release.yml"

clean:
	-rm -r dist/ *.egg-info/

ci: $(INCLUDE)/bitwuzla/bitwuzla.h

$(INCLUDE)/gmp.h:
	-rm -r $(DEPDIR)/gmp-6.2.1
	curl https://gmplib.org/download/gmp/gmp-6.2.1.tar.xz | tar xJC $(DEPDIR)
	cd $(DEPDIR)/gmp-6.2.1 && \
		./configure --enable-cxx --enable-fat && \
		make -j4 && make -j4 check && make install

$(INCLUDE)/bitwuzla/bitwuzla.h: $(INCLUDE)/gmp.h
	-rm -r $(DEPDIR)/bitwuzla $(REVISION).zip
	cd $(DEPDIR) && \
		curl -OL https://github.com/bitwuzla/bitwuzla/archive/$(REVISION).zip && \
		unzip $(REVISION).zip && \
		mv $(DEPDIR)/bitwuzla-$(REVISION) $(DEPDIR)/bitwuzla && \
		mkdir -p bitwuzla/.git && \
		echo "$(REVISION)" > bitwuzla/.git/HEAD && \
		rm $(REVISION).zip
	cd $(DEPDIR)/bitwuzla && \
		./contrib/setup-cadical.sh && \
		./contrib/setup-btor2tools.sh && \
		./contrib/setup-symfpu.sh && \
		./configure.sh --shared
	cd $(DEPDIR)/bitwuzla/build && make -j4 && make install
