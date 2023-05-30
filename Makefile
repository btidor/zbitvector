DEPDIR = /opt
INCLUDE = /usr/local/include
REVISION = 1230d80a5275ddf525da9c218c2bcd29c3130e49

.PHONY: all build clean ci pybitwuzla.pyi

all: build

build: clean
	python3 -m build

clean:
	-rm -r dist/ *.egg-info/

ci: $(INCLUDE)/bitwuzla/bitwuzla.h

$(INCLUDE)/gmp.h:
	-rm -r $(DEPDIR)/gmp-6.2.1
	curl https://gmplib.org/download/gmp/gmp-6.2.1.tar.xz | tar xJC $(DEPDIR)
	cd $(DEPDIR)/gmp-6.2.1 && \
		./configure --enable-cxx --enable-fat && \
		make && make check && make install

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
	cd $(DEPDIR)/bitwuzla/build && make && make install

pybitwuzla.pyi:
	pybitwuzla/stubs.py > $@
	black $@
