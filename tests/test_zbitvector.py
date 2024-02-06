from __future__ import annotations

from collections.abc import Hashable
from typing import Any, Literal, TypeVar, Union

import pytest

from zbitvector import Array, Constraint, Int, Solver, Uint
from zbitvector.conftest import Int8, Uint8, Uint64


def test_bitvector_validations():
    with pytest.raises(AttributeError, match="has no attribute '_sort'"):
        Int(123)

    IntA = Int[Union[Literal[32], Literal[64]]]  # ok
    with pytest.raises(AttributeError, match="has no attribute '_sort'"):
        IntA(123)

    K = TypeVar("K", bound=int)
    IntK = Int[K]  # type: ignore
    with pytest.raises(AttributeError, match="has no attribute '_sort'"):
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
    with pytest.raises(AttributeError, match="has no attribute '_sort'"):
        Array("A")

    IntA = Int[Union[Literal[32], Literal[64]]]
    Array[IntA, IntA]  # ok
    with pytest.raises(AttributeError, match="has no attribute '_sort'"):
        Array[IntA, IntA]("A")

    T = TypeVar("T", bound=Uint[Any])
    Array[T, T]  # type: ignore
    with pytest.raises(AttributeError, match="has no attribute '_sort'"):
        Array[T, T](123)  # type: ignore

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

    with pytest.raises(ValueError, match="already exists"):
        a, b = Uint8("XCE"), Int8("XCE")

    with pytest.raises(ValueError, match="already exists"):
        a, b = Uint8("YCE"), Uint64("YCE")

    with pytest.raises(ValueError, match="already exists"):
        a, b = Constraint("ZCE"), Uint8("ZCE")

    s = Solver()
    a, b = Array[Uint8, Uint8]("ACE"), Array[Uint8, Uint8]("ACE")
    s.add(a[Uint8(0)] != b[Uint8(0)])
    assert s.check() is False

    with pytest.raises(ValueError, match="already exists"):
        a, b = Array[Uint8, Uint8]("BCE"), Array[Int8, Int8]("BCE")


def test_uses_slots():
    for cls in (Constraint(True), Uint8(0), Int8(0), Array[Uint8, Uint8](Uint8(0))):
        assert not hasattr(cls, "__dict__")


def test_bool():
    with pytest.raises(TypeError, match="cannot use Constraint in a boolean context"):
        if Constraint(True):  # type: ignore
            pass

    if Uint8(0):  # allowed
        pass

    if Array[Uint8, Uint8]("BOOLA"):  # allowed
        pass


def test_hash():
    assert isinstance(Constraint(True), Hashable)
    assert isinstance(Uint8(0), Hashable)
    assert not isinstance(Array[Uint8, Uint8](Uint8(0)), Hashable)

    _ = {Constraint(True): 1}  # ok
    _ = {Uint8(0): 0}  # ok

    assert hash(Constraint(True)) != hash(Constraint(False))
    assert hash(Constraint(True)) == hash(~Constraint(False))
    assert hash(Uint8(0)) != hash(Uint8(1))
    assert hash(Uint8(0xFF)) == hash(~Uint8(0))

    # Make sure this raises an error both at runtime and from the typechecker:
    with pytest.raises(TypeError, match="unhashable type"):
        _ = {Array[Uint8, Uint8]("UHA"): 0}  # pyright: ignore[reportGeneralTypeIssues]


def test_array_equality():
    A = Array[Uint8, Uint8]("EQA")
    B = Array[Uint8, Uint8]("EQB")

    with pytest.raises(TypeError, match="arrays cannot be compared for equality"):
        if A == B:  # type: ignore
            pass


def test_ite_optimizations():
    t = Constraint("ITEA").ite(Uint8(0x7F), Uint8(0x1F))
    t = t >> Uint8(4)
    t = t >> Uint8(3)
    assert t.reveal() == 0

    t = Constraint("ITEA").ite(Uint8(0x7F), Uint8(0x1F))
    t = t >> Uint8(4)
    t = t.into(Uint64) >> Uint64(3)
    assert t.reveal() == 0

    t = Constraint("ITEA").ite(Uint8(0x7F), Uint8(0x1F))
    t = Constraint("ITEB").ite(t, Uint8(0))
    assert str(t).index("ITEB") < str(t).index("ITEA")


def test_shift_optimizations():
    v = Uint64("SHIFT")
    assert str(v << Uint64(8) << Uint64(8)) == str(v << Uint64(16))
    assert str(v >> Uint64(8) >> Uint64(8)) == str(v >> Uint64(16))

    assert (v << Uint64(8)).into(Uint8).reveal() == 0
    assert ((v & Uint64(0x00FFFFFFFFFFFFFF)) >> Uint64(56)).into(Uint8).reveal() == 0
    assert str((v >> Uint64(34)).into(Uint8)) == "Uint8(`((_ extract 41 34) SHIFT)`)"


def test_solver_validations():
    s = Solver()
    assert Uint8(1).reveal() == 1
    with pytest.raises(ValueError, match="solver is not ready for model evaluation"):
        s.evaluate(Uint8("X"))

    s.add(Uint8("X") + Uint8(1) == Uint8(0))
    assert Uint8(1).reveal() == 1
    with pytest.raises(ValueError, match="solver is not ready for model evaluation"):
        s.evaluate(Uint8("X"))

    assert s.check() is True
    assert Uint8(1).reveal() == 1
    assert s.evaluate(Uint8("X")) == 255
    assert Uint8(1).reveal() == 1

    t = Solver()
    t.add(Uint8("X") + Uint8(2) == Uint8(0))
    assert t.check() is True

    s.add(Constraint(True))
    assert Uint8(1).reveal() == 1
    with pytest.raises(ValueError, match="solver is not ready for model evaluation"):
        s.evaluate(Uint8("X"))
    assert t.evaluate(Uint8("X")) == 254
