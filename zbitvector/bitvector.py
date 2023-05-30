from __future__ import annotations

from typing import Any, cast

from typing_extensions import Self

from ._bitwuzla import Kind, ctx
from .constraint import Constraint
from .symbolic import Symbolic


class BitVector(Symbolic):
    def __init__(self, value: int | str) -> None:
        sort = ctx.bzla.mk_bv_sort(cast(Any, self).width)
        match value:
            case str():
                term = ctx.bzla.mk_const(sort, value)
            case int():
                term = ctx.bzla.mk_bv_value(sort, value)
        super().__init__(term)

    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self
    ) -> Constraint:
        return Constraint.from_expr(Kind.EQUAL, self._term, other._term)

    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self
    ) -> Constraint:
        return Constraint.from_expr(Kind.DISTINCT, self._term, other._term)

    def __add__(self, other: Self) -> Self:
        return self.from_expr(Kind.BV_ADD, self._term, other._term)

    def __sub__(self, other: Self) -> Self:
        return self.from_expr(Kind.BV_SUB, self._term, other._term)

    def __mul__(self, other: Self) -> Self:
        return self.from_expr(Kind.BV_MUL, self._term, other._term)

    def __lshift__(self: Self, other: Self) -> Self:
        return self.from_expr(Kind.BV_SHL, self._term, other._term)


class Uint(BitVector):
    def __init_subclass__(cls) -> None:
        if "width" not in dir(cls):
            raise AttributeError(f"subclass of Uint must define a 'width' attribute")
        width = cast(Any, cls).width
        if not isinstance(width, int):
            raise TypeError(f"expected Uint width to be an int, got: {repr(width)}")

    def __lt__(self: Self, other: Self) -> Constraint:
        return Constraint.from_expr(Kind.BV_ULT, self._term, other._term)

    def __le__(self: Self, other: Self) -> Constraint:
        return Constraint.from_expr(Kind.BV_ULE, self._term, other._term)

    def __floordiv__(self: Self, other: Self) -> Self:
        return self.from_expr(Kind.BV_UDIV, self._term, other._term)

    def __mod__(self: Self, other: Self) -> Self:
        return self.from_expr(Kind.BV_UREM, self._term, other._term)

    def __rshift__(self: Self, other: Self) -> Self:
        return self.from_expr(Kind.BV_SHR, self._term, other._term)

    def __and__(self: Self, other: Self) -> Self:
        return self.from_expr(Kind.BV_AND, self._term, other._term)

    def __or__(self: Self, other: Self) -> Self:
        return self.from_expr(Kind.BV_OR, self._term, other._term)

    def __xor__(self: Self, other: Self) -> Self:
        return self.from_expr(Kind.BV_XOR, self._term, other._term)

    def __invert__(self: Self) -> Self:
        return self.from_expr(Kind.BV_NOT, self._term)


class Int(BitVector):
    def __init_subclass__(cls) -> None:
        if "width" not in dir(cls):
            raise AttributeError(f"subclass of Int must define a 'width' attribute")
        width = cast(Any, cls).width
        if not isinstance(width, int):
            raise TypeError(f"expected Int width to be an int, got: {repr(width)}")

    def __lt__(self: Self, other: Self) -> Constraint:
        return Constraint.from_expr(Kind.BV_SLT, self._term, other._term)

    def __le__(self: Self, other: Self) -> Constraint:
        return Constraint.from_expr(Kind.BV_SLE, self._term, other._term)

    def __floordiv__(self: Self, other: Self) -> Self:
        return self.from_expr(Kind.BV_SDIV, self._term, other._term)

    def __mod__(self: Self, other: Self) -> Self:
        return self.from_expr(Kind.BV_SREM, self._term, other._term)

    def __rshift__(self: Self, other: Self) -> Self:
        return self.from_expr(Kind.BV_ASHR, self._term, other._term)
