DEPDIR = /opt
INCLUDE = /usr/local/include
REVISION = 1230d80a5275ddf525da9c218c2bcd29c3130e49

# Workaround for error "Compatibility with CMake < 3.5 has been removed from
# CMake".
export CMAKE_POLICY_VERSION_MINIMUM = 3.5

.PHONY: all build clean ci docs release

all: build

build: clean
	python3 -m build
	auditwheel repair --plat auto dist/*.whl -w dist/

docs:
	make -C docs clean
	ZBITVECTOR_SOLVER=dummy O=-W make -C docs html
	python3 -m http.server --directory docs/_build/html/

release:
	@bash -c '[[ "$V" =~ ^[0-9]+\.[0-9]+\.[0-9]+$$ ]] || \
		(echo "usage: make release V=x.y.z"; exit 1)'
	@bash -c 'read -p "Release v$V? " -n 1 -r && echo && \
		([[ $${REPLY^^} == "Y" ]] || exit 2)'
	git tag -s "v$V" -m "zbitvector@v$V"
	git push origin "v$V"
	@echo "\n1. Wait for build"
	@echo "2. Check artifacts"
	@echo "3. Approve workflow"
	@echo "4. Publish draft release"
	@echo "\n  https://github.com/btidor/zbitvector/actions/workflows/build.yml\n"

clean:
	-rm -r dist/ *.egg-info/

ci: $(INCLUDE)/bitwuzla/bitwuzla.h

# FYI, gmplib.org blocks GitHub Actions/Azure, so we have to use a mirror...

$(INCLUDE)/gmp.h:
	-rm -r $(DEPDIR)/gmp-6.3.0
	curl https://misc.btidor.dev/gmp-6.3.0.tar.xz | tar xJC $(DEPDIR)
	cd $(DEPDIR)/gmp-6.3.0 && \
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
		sed -i -e 's/db46e96d1bc26271cf32849592e7db1c702a7bc1/a1bb693253c6d2e7b76bf3871438e875145d41a9/' \
			contrib/setup-btor2tools.sh && \
		./contrib/setup-cadical.sh && \
		./contrib/setup-btor2tools.sh && \
		./contrib/setup-symfpu.sh && \
		./configure.sh --shared
	cd $(DEPDIR)/bitwuzla/build && make -j4 && make install
	touch -c $@  # fix mtime (for macOS)
