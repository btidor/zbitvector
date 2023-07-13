"""Backend implementation for the Z3 solver."""

from __future__ import annotations

import abc
from typing import Any, Callable, Final, Generic, TypeVar

import z3
from typing_extensions import Never, Self

from ._util import BitVectorMeta

# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingTypeStubs=false

CTX = z3.Z3_mk_context(z3.Z3_mk_config())

N = TypeVar("N", bound=int)
M = TypeVar("M", bound=int)


class Symbolic(abc.ABC):
    __slots__ = ("_term",)

    @abc.abstractmethod
    def __init__(self, term: Any, /) -> None:
        self._term: Final[Any] = term

    @classmethod
    def _from_expr(cls, kind: Callable[..., Any], *syms: Symbolic) -> Self:
        term = kind(CTX, *(s._term for s in syms))
        term = z3.Z3_simplify(CTX, term)
        result = cls.__new__(cls)
        Symbolic.__init__(result, term)
        return result

    @classmethod
    def _from_expr_tuple(cls, kind: Callable[..., Any], *syms: Symbolic) -> Self:
        args = (z3.Ast * len(syms))(*(s._term for s in syms))
        term = kind(CTX, len(syms), args)
        term = z3.Z3_simplify(CTX, term)
        result = cls.__new__(cls)
        Symbolic.__init__(result, term)
        return result

    # Symbolic instances are immutable. For performance, don't copy them.
    def __copy__(self) -> Self:
        return self

    def __deepcopy__(self, memo: Any, /) -> Self:
        return self

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(`{z3.Z3_ast_to_string(CTX, self._term)}`)"

    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self, /
    ) -> Constraint:
        return Constraint._from_expr(z3.Z3_mk_eq, self, other)

    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self, /
    ) -> Constraint:
        return Constraint._from_expr_tuple(z3.Z3_mk_distinct, self, other)


class Constraint(Symbolic):
    _sort: Final[Any] = z3.Z3_mk_bool_sort(CTX)
    __slots__ = ()

    def __init__(self, value: bool | str, /):
        if isinstance(value, str):
            term = z3.Z3_mk_const(CTX, z3.Z3_mk_string_symbol(CTX, value), self._sort)
        else:
            term = z3.Z3_mk_true(CTX) if value else z3.Z3_mk_false(CTX)
        Symbolic.__init__(self, term)

    def __invert__(self) -> Self:
        return self._from_expr(z3.Z3_mk_not, self)

    def __and__(self, other: Self, /) -> Self:
        return self._from_expr_tuple(z3.Z3_mk_and, self, other)

    def __or__(self, other: Self, /) -> Self:
        return self._from_expr_tuple(z3.Z3_mk_or, self, other)

    def __xor__(self, other: Self, /) -> Self:
        return self._from_expr(z3.Z3_mk_xor, self, other)

    def __bool__(self) -> Never:
        raise TypeError("cannot use Constraint in a boolean context")

    def ite(self, then: Symbolic, else_: Symbolic, /) -> Symbolic:
        return then._from_expr(z3.Z3_mk_ite, self, then, else_)


class BitVector(Symbolic, Generic[N], metaclass=BitVectorMeta):
    width: Final[int]  # type: ignore
    _sort: Final[Any]  # type: ignore
    __slots__ = ()

    def __init__(self, value: int | str, /) -> None:
        if isinstance(value, str):
            term = z3.Z3_mk_const(CTX, z3.Z3_mk_string_symbol(CTX, value), self._sort)
        else:
            term = z3.Z3_mk_numeral(CTX, str(value), self._sort)
        Symbolic.__init__(self, term)

    @classmethod
    def _make_sort(cls, width: int) -> Any:
        return z3.Z3_mk_bv_sort(CTX, width)

    @abc.abstractmethod
    def __lt__(self, other: Self, /) -> Constraint:
        ...

    @abc.abstractmethod
    def __le__(self, other: Self, /) -> Constraint:
        ...

    def __invert__(self) -> Self:
        return self._from_expr(z3.Z3_mk_bvnot, self)

    def __and__(self, other: Self, /) -> Self:
        return self._from_expr(z3.Z3_mk_bvand, self, other)

    def __or__(self, other: Self, /) -> Self:
        return self._from_expr(z3.Z3_mk_bvor, self, other)

    def __xor__(self, other: Self, /) -> Self:
        return self._from_expr(z3.Z3_mk_bvxor, self, other)

    def __add__(self, other: Self, /) -> Self:
        return self._from_expr(z3.Z3_mk_bvadd, self, other)

    def __sub__(self, other: Self, /) -> Self:
        return self._from_expr(z3.Z3_mk_bvsub, self, other)

    def __mul__(self, other: Self, /) -> Self:
        return self._from_expr(z3.Z3_mk_bvmul, self, other)

    @abc.abstractmethod
    def __truediv__(self, other: Self, /) -> Self:
        ...

    @abc.abstractmethod
    def __mod__(self, other: Self, /) -> Self:
        ...

    def __lshift__(self, other: Uint[N], /) -> Self:
        return self._from_expr(z3.Z3_mk_bvshl, self, other)

    @abc.abstractmethod
    def __rshift__(self, other: Uint[N], /) -> Self:
        ...


class Uint(BitVector[N]):
    __slots__ = ()

    def __lt__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(z3.Z3_mk_bvult, self, other)

    def __le__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(z3.Z3_mk_bvule, self, other)

    def __truediv__(self, other: Self, /) -> Self:
        return self._from_expr(z3.Z3_mk_bvudiv, self, other)

    def __mod__(self, other: Self, /) -> Self:
        return self._from_expr(z3.Z3_mk_bvurem, self, other)

    def __rshift__(self, other: Uint[N], /) -> Self:
        return self._from_expr(z3.Z3_mk_bvlshr, self, other)

    def into(self, other: type[BitVector[M]], /) -> BitVector[M]:
        if self.width < other.width:
            term = z3.Z3_mk_zero_ext(CTX, other.width - self.width, self._term)
        elif self.width > other.width:
            term = z3.Z3_mk_extract(CTX, other.width - 1, 0, self._term)
        else:
            term = self._term
        term = z3.Z3_simplify(CTX, term)
        result = other.__new__(other)
        Symbolic.__init__(result, term)
        return result


class Int(BitVector[N]):
    __slots__ = ()

    def __lt__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(z3.Z3_mk_bvslt, self, other)

    def __le__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(z3.Z3_mk_bvsle, self, other)

    def __truediv__(self, other: Self, /) -> Self:
        return self._from_expr(z3.Z3_mk_bvsdiv, self, other)

    def __mod__(self, other: Self, /) -> Self:
        return self._from_expr(z3.Z3_mk_bvsrem, self, other)

    def __rshift__(self, other: Uint[N], /) -> Self:
        return self._from_expr(z3.Z3_mk_bvashr, self, other)

    def into(self, other: type[BitVector[M]], /) -> BitVector[M]:
        if self.width < other.width:
            term = z3.Z3_mk_sign_ext(CTX, other.width - self.width, self._term)
        elif self.width > other.width:
            term = z3.Z3_mk_extract(CTX, other.width - 1, 0, self._term)
        else:
            term = self._term
        term = z3.Z3_simplify(CTX, term)
        result = other.__new__(other)
        Symbolic.__init__(result, term)
        return result
