#!/usr/bin/env pytest

from .bitvector import Uint


class Uint8(Uint):
    width = 8


def test_add():
    c = Uint8(1) == Uint8(2)
    assert c.smtlib() == "false"
