#!/usr/bin/env pytest

from . import Uint8


def test_add():
    c = Uint8(1) == Uint8(2)
    assert c.smtlib() == "false"
