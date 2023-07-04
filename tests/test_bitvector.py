#!/usr/bin/env pytest

import typing

import pytest

import zbitvector
from zbitvector.conftest import Uint8


def test_add():
    c = Uint8(1) == Uint8(2)
    assert c.smtlib() == "false"


def test_init_validations():
    with pytest.raises(TypeError, match=f"Cannot instantiate Int directly"):
        zbitvector.Int(123)

    with pytest.raises(TypeError, match="Unknown type parameter passed to Int"):
        zbitvector.Int[typing.Literal["asdf"]]  # type: ignore

    with pytest.raises(TypeError, match="Int requires a positive width"):
        zbitvector.Int[typing.Literal[-1]]
