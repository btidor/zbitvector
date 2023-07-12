#!/usr/bin/env pytest

from __future__ import annotations

import inspect
import re
from collections.abc import Hashable
from types import ModuleType
from typing import Literal, TypeVar, Union

import pytest

from zbitvector import _backend  # pyright: ignore[reportPrivateUsage]
from zbitvector import Constraint, Int, _zbitvector
from zbitvector.conftest import Int8, Uint8


def test_init_validations():
    with pytest.raises(AttributeError, match=f"has no attribute '_sort'"):
        Int(123)

    IntA = Int[Union[Literal[32], Literal[64]]]
    with pytest.raises(AttributeError, match=f"has no attribute '_sort'"):
        IntA(123)

    K = TypeVar("K", bound=int)
    IntK = Int[K]
    with pytest.raises(AttributeError, match=f"has no attribute '_sort'"):
        IntK(123)

    with pytest.raises(
        TypeError,
        match=r"integer passed to Int\[...\]; use Int\[Literal\[5\]\] instead",
    ):
        Int[5]  # type: ignore

    with pytest.raises(TypeError, match="unsupported type parameter passed to Int"):
        Int[Literal["asdf"]]  # type: ignore

    with pytest.raises(TypeError, match="Int requires a positive width"):
        Int[Literal[-1]]

    Int8 = Int[Literal[8]]
    Int8(123)
    assert re.match(r"<class 'zbitvector.(_bitwuzla|_z3).Int8'>", repr(Int8))


def test_backend_api():
    assert _enumerate_module(_backend) == _enumerate_module(_zbitvector)


def _enumerate_module(module: ModuleType) -> set[str]:
    results: set[str] = set()
    for _, c in inspect.getmembers(module):
        if not inspect.isclass(c):
            continue
        if inspect.getmodule(c) != inspect.getmodule(module):
            continue
        for _, f in inspect.getmembers(c):
            if not inspect.isfunction(f):
                continue
            if f.__name__.startswith("_") and not f.__name__.startswith("__"):
                continue
            if c.__name__ == "Symbolic" and f.__name__ == "__init__":
                # This initializer takes a backend-specific type, but it's
                # hidden from private subclasses.
                continue
            results.add(f"{c.__name__}.{f.__name__}{inspect.signature(f)}")
    return results


def test_uses_slots():
    for cls in (Constraint(True), Uint8(0), Int8(0)):
        assert not hasattr(cls, "__dict__")


def test_bool():
    with pytest.raises(TypeError, match="cannot use Constraint in a boolean context"):
        if Constraint(True):  # type: ignore
            pass

    if Uint8(0):  # allowed
        pass


def test_hash():
    assert not isinstance(Constraint(True), Hashable)
    assert not isinstance(Uint8(0), Hashable)

    # Make sure these raise an error both at runtime and from the typechecker:
    with pytest.raises(TypeError, match="unhashable type"):
        _ = {Constraint(True): 1}  # pyright: ignore[reportGeneralTypeIssues]
    with pytest.raises(TypeError, match="unhashable type"):
        _ = {Uint8(0): 0}  # pyright: ignore[reportGeneralTypeIssues]
