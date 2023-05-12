DEPDIR = /opt
REVISION = 1230d80a5275ddf525da9c218c2bcd29c3130e49

.PHONY: all build setup libbitwuzla

all: build

build:
	python3 -m build

setup:
	yum install -y gmp-devel || apk add gmp-dev

libbitwuzla: setup
	git clone https://github.com/bitwuzla/bitwuzla $(DEPDIR)/bitwuzla
	cd $(DEPDIR)/bitwuzla && git checkout $(REVISION) && \
		./contrib/setup-cadical.sh && \
		./contrib/setup-btor2tools.sh && \
		./contrib/setup-symfpu.sh && \
		./configure.sh --shared
	cd $(DEPDIR)/bitwuzla/build && make && make install
