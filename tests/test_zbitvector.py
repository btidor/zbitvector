from __future__ import annotations

from collections.abc import Hashable
from typing import Any, Literal, TypeVar, Union

import pytest

# pyright: reportWildcardImportFromLibrary=false
from zbitvector import *
from zbitvector.conftest import Int8, Uint8, Uint64


def test_bitvector_validations():
    with pytest.raises(AttributeError, match=f"has no attribute '_sort'"):
        Int(123)

    IntA = Int[Union[Literal[32], Literal[64]]]  # ok
    with pytest.raises(AttributeError, match=f"has no attribute '_sort'"):
        IntA(123)

    K = TypeVar("K", bound=int)
    IntK = Int[K]  # ok
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

    Int8(123)
    assert repr(Int8) == "<class 'zbitvector.Int8'>"


def test_array_validations():
    with pytest.raises(AttributeError, match=f"has no attribute '_sort'"):
        Array("A")

    IntA = Int[Union[Literal[32], Literal[64]]]
    Array[IntA, IntA]  # ok
    with pytest.raises(AttributeError, match=f"has no attribute '_sort'"):
        Array[IntA, IntA]("A")

    T = TypeVar("T", bound=Uint[Any])
    Array[T, T]  # ok
    with pytest.raises(AttributeError, match=f"has no attribute '_sort'"):
        Array[T, T](123)

    with pytest.raises(
        TypeError,
        match=r"expected a pair of types",
    ):
        Array[Uint8]  # type: ignore

    with pytest.raises(
        TypeError,
        match=r"expected a pair of types",
    ):
        Array[Uint8, Uint8, Uint8]  # type: ignore

    with pytest.raises(TypeError, match="unsupported type parameter passed to Array"):
        Array[Literal["asdf"], Uint8]  # type: ignore

    with pytest.raises(TypeError, match="unsupported type parameter passed to Array"):
        Array[8, 64]  # type: ignore

    Array[Uint8, Uint64](Uint64(0))
    assert repr(Array[Uint8, Uint64]) == "<class 'zbitvector.Array[Uint8, Uint64]'>"


def test_constants_equal():
    s = Solver()
    a, b = Uint8("UCE"), Uint8("UCE")  # the *same* constant
    s.add(a != b)
    assert s.check() is False


def test_uses_slots():
    for cls in (Constraint(True), Uint8(0), Int8(0), Array[Uint8, Uint8]("A")):
        assert not hasattr(cls, "__dict__")


def test_bool():
    with pytest.raises(TypeError, match="cannot use Constraint in a boolean context"):
        if Constraint(True):  # type: ignore
            pass

    if Uint8(0):  # allowed
        pass

    if Array[Uint8, Uint8]("A"):  # allowed
        pass


def test_hash():
    assert not isinstance(Constraint(True), Hashable)
    assert not isinstance(Uint8(0), Hashable)
    assert not isinstance(Array[Uint8, Uint8]("A"), Hashable)

    # Make sure these raise an error both at runtime and from the typechecker:
    with pytest.raises(TypeError, match="unhashable type"):
        _ = {Constraint(True): 1}  # pyright: ignore[reportGeneralTypeIssues]
    with pytest.raises(TypeError, match="unhashable type"):
        _ = {Uint8(0): 0}  # pyright: ignore[reportGeneralTypeIssues]
    with pytest.raises(TypeError, match="unhashable type"):
        _ = {Array[Uint8, Uint8]("A"): 0}  # pyright: ignore[reportGeneralTypeIssues]


def test_array_equality():
    A = Array[Uint8, Uint8]("A")
    B = Array[Uint8, Uint8]("B")

    with pytest.raises(TypeError, match="arrays cannot be compared for equality"):
        if A == B:  # type: ignore
            pass
