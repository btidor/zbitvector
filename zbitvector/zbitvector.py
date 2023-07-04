from __future__ import annotations

import abc
from typing import Final, Generic, TypeVar, get_args

from typing_extensions import Self, assert_never

from ._bitwuzla import BitwuzlaTerm, Kind, ctx


class Symbolic(abc.ABC):
    _term: Final[BitwuzlaTerm]

    @abc.abstractmethod
    def __init__(self, term: BitwuzlaTerm) -> None:
        self._term = term

    @classmethod
    def from_expr(cls, kind: Kind, *terms: BitwuzlaTerm) -> Self:
        term = ctx.bzla.mk_term(kind, terms)
        result = cls.__new__(cls)
        Symbolic.__init__(result, term)
        return result

    def __copy__(self) -> Self:
        return self

    def __deepcopy__(self) -> Self:
        return self

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(`{self.smtlib()}`)"

    def smtlib(self) -> str:
        return self._term.dump("smt2")


S = TypeVar("S", bound=Symbolic)


class Constraint(Symbolic):
    def __init__(self, value: bool | str):
        if isinstance(value, str):
            term = ctx.bzla.mk_const(ctx.bool_sort, value)
        elif isinstance(value, bool):  # pyright: ignore[reportUnnecessaryIsInstance]
            term = ctx.bzla.mk_bv_value(ctx.bool_sort, value)
        else:
            assert_never(value)
        super().__init__(term)

    def __invert__(self) -> Constraint:
        return self.from_expr(Kind.NOT, self._term)

    def ite(self, then: S, else_: S) -> S:
        return then.from_expr(Kind.ITE, self._term, then._term, else_._term)


N = TypeVar("N", bound=int)


class BitVector(Symbolic, Generic[N]):
    _width: Final[int] = 0

    def __class_getitem__(cls, key: TypeVar) -> type[Self]:
        args = get_args(key)
        if len(args) == 0:
            return cls
        elif len(args) == 1 and isinstance(args[0], int):
            if args[0] <= 0:
                raise TypeError(f"{cls.__name__} requires a positive width.")

            def construct(value: int | str) -> Self:
                # Create and initialize a new Int/Uint, with one customization:
                # we manually specify the instance's _width attribute before
                # calling __init__.
                instance = cls.__new__(cls)
                instance._width = args[0]  # pyright: ignore[reportGeneralTypeIssues]
                instance.__init__(value)
                return instance

            return construct  # type: ignore
        else:
            raise TypeError(f"Unknown type parameter passed to {cls.__name__}[...].")

    def __init__(self, value: int | str) -> None:
        if self._width == 0:
            raise TypeError(
                f"Cannot instantiate {self.__class__.__name__} directly; "
                f"use {self.__class__.__name__}[N](...) instead."
            )
        sort = ctx.bzla.mk_bv_sort(self._width)
        if isinstance(value, str):
            term = ctx.bzla.mk_const(sort, value)
        elif isinstance(value, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            term = ctx.bzla.mk_bv_value(sort, value)
        else:
            assert_never(value)
        super().__init__(term)

    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self
    ) -> Constraint:
        """
        >>> Uint8(1) == Uint8(3)
        Constraint(`false`)
        """
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


class Uint(BitVector[N]):
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


class Int(BitVector[N]):
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
