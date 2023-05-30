TARGETS = bitwuzla_api.pxd \
	pybitwuzla_abort.cpp \
	pybitwuzla_abort.h \
	pybitwuzla_enums.pxd \
	pybitwuzla.pyx

CHECKOUT=/opt/bitwuzla
REVFILE = $(CHECKOUT)/.git/HEAD

HEADER = Generated from https://github.com/bitwuzla/bitwuzla \
	at $(shell cat $(REVFILE) | cut -c 1-7)

.PHONY: all clean stubs ../pybitwuzla.pyi
.EXTRA_PREREQS:= $(abspath $(lastword $(MAKEFILE_LIST))) $(REVFILE)

all: $(TARGETS)

clean:
	-rm $(TARGETS)
	-rm ../pybitwuzla.pyi

stubs: ../pybitwuzla.pyi

pybitwuzla_enums.pxd: $(CHECKOUT)/src/api/python/mkenums.py $(CHECKOUT)/src/api/c/bitwuzla.h
	python3 $^ $@
	sed -i '1 i\# $(HEADER)\n' $@
	patch < pybitwuzla_enums.diff

../pybitwuzla.pyi: stubs.py
	python3 $< > $@
	sed -i '1 i\# $(HEADER)\n' $@
	black $@

%.h: $(CHECKOUT)/src/api/python/%.h
	cp $< $@
	sed -i '1 i\// $(HEADER)\n' $@

%.cpp: $(CHECKOUT)/src/api/python/%.cpp %.diff
	cp $< $@
	sed -i '1 i\// $(HEADER)\n' $@
	patch < $(word 2,$^)

%.pxd: $(CHECKOUT)/src/api/python/%.pxd %.diff
	cp $< $@
	sed -i '1 i\# $(HEADER)\n' $@
	patch < $(word 2,$^)

%.pyx: $(CHECKOUT)/src/api/python/%.pyx %.diff
	cp $< $@
	sed -i '1 i\# $(HEADER)\n' $@
	patch < $(word 2,$^)
