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
	-rm *.orig *.rej
	-rm ../pybitwuzla.pyi

stubs: ../pybitwuzla.pyi

pybitwuzla_enums.pxd: $(CHECKOUT)/src/api/python/mkenums.py $(CHECKOUT)/src/api/c/bitwuzla.h
	python3 $^ $@
	patch < pybitwuzla_enums.diff
	sed -i '1 i\# $(HEADER)\n' $@

../pybitwuzla.pyi: stubs.py
	python3 $< > $@
	sed -i '1 i\# $(HEADER)\n' $@
	black $@

%.h: $(CHECKOUT)/src/api/python/%.h
	cp $< $@
	sed -i '1 i\// $(HEADER)\n' $@

%.cpp: $(CHECKOUT)/src/api/python/%.cpp %.diff
	cp $< $@
	patch < $(word 2,$^)
	sed -i '1 i\// $(HEADER)\n' $@

%.pxd: $(CHECKOUT)/src/api/python/%.pxd %.diff
	cp $< $@
	patch < $(word 2,$^)
	sed -i '1 i\# $(HEADER)\n' $@

%.pyx: $(CHECKOUT)/src/api/python/%.pyx %.diff
	cp $< $@
	patch < $(word 2,$^)
	sed -i '1 i\# $(HEADER)\n' $@
