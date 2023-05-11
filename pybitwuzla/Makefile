TARGETS = pybitwuzla_abort.cpp \
	pybitwuzla_enums.pxd \
	pybitwuzla_utils.c \
	pybitwuzla.pyx

CHECKOUT=/opt/bitwuzla
REVFILE = $(CHECKOUT)/.git/HEAD

HEADER = Generated from https://github.com/bitwuzla/bitwuzla \
	at $(shell cat $(REVFILE) | cut -c 1-7)

.PHONY: all clean
.EXTRA_PREREQS:= $(abspath $(lastword $(MAKEFILE_LIST))) $(REVFILE)

all: $(TARGETS)

clean:
	-rm $(TARGETS)

pybitwuzla_enums.pxd: $(CHECKOUT)/src/api/python/mkenums.py $(CHECKOUT)/src/api/c/bitwuzla.h
	python3 $^ $@
	sed -i '1 i\# $(HEADER)\n' $@

%.c: $(CHECKOUT)/src/api/python/%.c
	cp $< $@
	sed -i '1 i\// $(HEADER)\n' $@

%.cpp: $(CHECKOUT)/src/api/python/%.cpp
	cp $< $@
	sed -i '1 i\// $(HEADER)\n' $@

%.pyx: $(CHECKOUT)/src/api/python/%.pyx
	cp $< $@
	sed -i '1 i\# $(HEADER)\n' $@
