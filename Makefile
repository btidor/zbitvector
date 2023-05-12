DEPDIR = /opt
REVISION = 1230d80a5275ddf525da9c218c2bcd29c3130e49

.PHONY: all build clean libgmp libbitwuzla

all: build

build: clean
	python3 -m build

clean:
	-rm -r dist/ *.egg-info/

libgmp:
	curl https://gmplib.org/download/gmp/gmp-6.2.1.tar.xz | tar xJC $(DEPDIR)
	cd $(DEPDIR)/gmp-6.2.1 && \
		./configure --enable-cxx --enable-fat && \
		make && make check && make install

libbitwuzla: libgmp
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
