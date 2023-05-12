DEPDIR = /opt
REVISION = 1230d80a5275ddf525da9c218c2bcd29c3130e49

.PHONY: all build libgmp libbitwuzla

all: build

build:
	python3 -m build

libgmp:
	curl https://gmplib.org/download/gmp/gmp-6.2.1.tar.xz | tar xJC $(DEPDIR)
	cd $(DEPDIR)/gmp-6.2.1 && \
		./configure --enable-cxx --enable-fat && \
		make && make check && make install

libbitwuzla: libgmp
	git clone https://github.com/bitwuzla/bitwuzla $(DEPDIR)/bitwuzla
	cd $(DEPDIR)/bitwuzla && git checkout $(REVISION) && \
		./contrib/setup-cadical.sh && \
		./contrib/setup-btor2tools.sh && \
		./contrib/setup-symfpu.sh && \
		./configure.sh --shared
	cd $(DEPDIR)/bitwuzla/build && make && make install
