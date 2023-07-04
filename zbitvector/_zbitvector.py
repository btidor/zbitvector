from __future__ import annotations

import abc
from typing import Final, Generic, TypeVar, get_args, overload

from typing_extensions import Self, assert_never, override

from ._bitwuzla import BitwuzlaTerm, Kind, ctx

N = TypeVar("N", bound=int)


class Symbolic(abc.ABC):
    _term: Final[BitwuzlaTerm]

    @abc.abstractmethod
    def __init__(self, term: BitwuzlaTerm, /) -> None:
        self._term = term

    @classmethod
    def _from_expr(cls, kind: Kind, *syms: Symbolic) -> Self:
        term = ctx.bzla.mk_term(kind, tuple(s._term for s in syms))
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

    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self, /
    ) -> Constraint:
        """
        >>> Uint8(1) == Uint8(3)
        Constraint(`false`)
        """
        return Constraint._from_expr(Kind.EQUAL, self, other)

    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self, /
    ) -> Constraint:
        return Constraint._from_expr(Kind.DISTINCT, self, other)


class Constraint(Symbolic):
    def __init__(self, value: bool | str, /):
        if isinstance(value, str):
            term = ctx.bzla.mk_const(ctx.bool_sort, value)
        elif isinstance(value, bool):  # pyright: ignore[reportUnnecessaryIsInstance]
            term = ctx.bzla.mk_bv_value(ctx.bool_sort, value)
        else:
            assert_never(value)
        super().__init__(term)

    def __invert__(self) -> Self:
        return self._from_expr(Kind.NOT, self)

    def __and__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.AND, self, other)

    def __or__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.OR, self, other)

    def __xor__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.XOR, self, other)

    @overload
    def ite(self, then: Uint[N], else_: Uint[N]) -> Uint[N]:
        ...

    @overload
    def ite(self, then: Int[N], else_: Int[N]) -> Int[N]:
        ...

    @overload
    def ite(self, then: Constraint, else_: Constraint) -> Constraint:
        ...

    def ite(self, then: Symbolic, else_: Symbolic) -> Symbolic:
        return then._from_expr(Kind.ITE, self, then, else_)


class BitVector(Symbolic, Generic[N]):
    _width: Final[int] = 0

    def __class_getitem__(cls, key: TypeVar, /) -> type[Self]:
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

    def __init__(self, value: int | str, /) -> None:
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

    @override
    @classmethod
    def _from_expr(cls, kind: Kind, *syms: Symbolic) -> Self:
        assert isinstance(syms[-1], BitVector)
        result = super()._from_expr(kind, *syms)
        result._width = syms[-1]._width  # type: ignore
        return result

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self._width}(`{self.smtlib()}`)"

    @abc.abstractmethod
    def __lt__(self, other: Self, /) -> Constraint:
        ...

    @abc.abstractmethod
    def __le__(self, other: Self, /) -> Constraint:
        ...

    def __invert__(self) -> Self:
        return self._from_expr(Kind.BV_NOT, self)

    def __and__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_AND, self, other)

    def __or__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_OR, self, other)

    def __xor__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_XOR, self, other)

    def __add__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_ADD, self, other)

    def __sub__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_SUB, self, other)

    def __mul__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_MUL, self, other)

    @abc.abstractmethod
    def __floordiv__(self, other: Self, /) -> Self:
        ...

    @abc.abstractmethod
    def __mod__(self, other: Self, /) -> Self:
        ...

    def __lshift__(self, other: Uint[N], /) -> Self:
        return self._from_expr(Kind.BV_SHL, self, other)

    @abc.abstractmethod
    def __rshift__(self, other: Uint[N], /) -> Self:
        ...


class Uint(BitVector[N]):
    def __lt__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(Kind.BV_ULT, self, other)

    def __le__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(Kind.BV_ULE, self, other)

    def __floordiv__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_UDIV, self, other)

    def __mod__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_UREM, self, other)

    def __rshift__(self, other: Uint[N], /) -> Self:
        return self._from_expr(Kind.BV_SHR, self, other)


class Int(BitVector[N]):
    def __lt__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(Kind.BV_SLT, self, other)

    def __le__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(Kind.BV_SLE, self, other)

    def __floordiv__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_SDIV, self, other)

    def __mod__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_SREM, self, other)

    def __rshift__(self, other: Uint[N], /) -> Self:
        return self._from_expr(Kind.BV_ASHR, self, other)
