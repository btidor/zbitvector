"""Backend implementation for the Z3 solver."""

from __future__ import annotations

import abc
from typing import Any, Callable, Dict, Final, Generic, Tuple, TypeVar, Union

import z3
from typing_extensions import Never, Self

from ._util import ArrayMeta, BitVectorMeta

# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportMissingTypeStubs=false

CTX = z3.Z3_mk_context(z3.Z3_mk_config())

N = TypeVar("N", bound=int)
M = TypeVar("M", bound=int)

CACHE: Dict[str, Tuple[type, Any]] = {}


def _mk_const(instance: Symbolic | Array[K, V], name: str) -> Any:
    if name not in CACHE:
        term = z3.Z3_mk_const(
            CTX,
            z3.Z3_mk_string_symbol(CTX, name),
            instance._sort,  # pyright: ignore[reportPrivateUsage]
        )
        CACHE[name] = (instance.__class__, term)
    cls, term = CACHE[name]
    if not isinstance(instance, cls):
        raise ValueError(
            f'cannot create {instance.__class__.__name__}("{name}") '
            f'because {cls.__name__}("{name}") already exists'
        )
    return term


class Symbolic(abc.ABC):
    _sort: Any
    __slots__ = ("_term",)

    @abc.abstractmethod
    def __init__(self, term: Any, /) -> None:
        self._term: Any = term

    @classmethod
    def _from_expr(
        cls, kind: Callable[..., Any], *syms: Symbolic | Array[K, V]
    ) -> Self:
        term = kind(
            CTX, *(s._term for s in syms)  # pyright: ignore[reportPrivateUsage]
        )
        term = z3.Z3_simplify(CTX, term)
        result = cls.__new__(cls)
        Symbolic.__init__(result, term)
        return result

    @classmethod
    def _from_expr_tuple(
        cls, kind: Callable[..., Any], *syms: Symbolic | Array[K, V]
    ) -> Self:
        args = (z3.Ast * len(syms))(
            *(s._term for s in syms)  # pyright: ignore[reportPrivateUsage]
        )
        term = kind(CTX, len(syms), args)
        term = z3.Z3_simplify(CTX, term)
        result = cls.__new__(cls)
        Symbolic.__init__(result, term)
        return result

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
            term = _mk_const(self, value)
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
            term = _mk_const(self, value)
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


K = TypeVar("K", bound=Union[Uint[Any], Int[Any]])
V = TypeVar("V", bound=Union[Uint[Any], Int[Any]])


class Array(Generic[K, V], metaclass=ArrayMeta):
    _key: type[K]
    _value: type[V]
    _sort: Any
    __slots__ = ("_term",)

    def __init__(self, value: V | str, /) -> None:
        if isinstance(value, str):
            term = _mk_const(self, value)
        else:
            self._sort  # for error message consistency
            term = z3.Z3_mk_const_array(
                CTX, self._key._sort, value._term  # pyright: ignore[reportPrivateUsage]
            )
        self._term = term

    @classmethod
    def _make_sort(cls, key: K, value: V) -> Any:
        return z3.Z3_mk_array_sort(
            CTX, key._sort, value._sort  # pyright: ignore[reportPrivateUsage]
        )

    def __copy__(self) -> Self:
        result = self.__new__(self.__class__)
        result._term = self._term
        return result

    def __deepcopy__(self, memo: Any, /) -> Self:
        return self.__copy__()

    def __repr__(self) -> str:
        render = self._term
        decl = z3.Z3_get_app_decl(CTX, self._term)
        if z3.Z3_get_decl_kind(CTX, decl) == z3.Z3_OP_CONST_ARRAY:
            render = z3.Z3_get_app_arg(CTX, self._term, 0)
        return f"{self.__class__.__name__}(`{z3.Z3_ast_to_string(CTX, render)}`)"

    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Never, /
    ) -> Never:
        raise TypeError(f"arrays cannot be compared for equality.")

    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Never, /
    ) -> Never:
        raise TypeError(f"arrays cannot be compared for equality.")

    def __getitem__(self, key: K) -> V:
        return self._value._from_expr(  # pyright: ignore[reportPrivateUsage]
            z3.Z3_mk_select, self, key
        )

    def __setitem__(self, key: K, value: V) -> None:
        self._term = z3.Z3_simplify(
            CTX,
            z3.Z3_mk_store(
                CTX,
                self._term,
                key._term,  # pyright: ignore[reportPrivateUsage]
                value._term,  # pyright: ignore[reportPrivateUsage]
            ),
        )


class Solver:
    __slots__ = ("_solver",)

    def __init__(self) -> None:
        self._solver = z3.Z3_mk_solver(CTX)

    def add(self, assertion: Constraint, /) -> None:
        z3.Z3_solver_assert(
            CTX, self._solver, assertion._term  # pyright: ignore[reportPrivateUsage]
        )

    def check(self, *assumptions: Constraint) -> bool:
        arr = (z3.Ast * len(assumptions))(
            *(a._term for a in assumptions)  # pyright: ignore[reportPrivateUsage]
        )
        r = z3.Z3_solver_check_assumptions(CTX, self._solver, len(assumptions), arr)
        if r == z3.Z3_L_TRUE:
            return True
        elif r == z3.Z3_L_FALSE:
            return False
        else:
            reason = z3.Z3_solver_get_reason_unknown(CTX, self._solver)
            raise RuntimeError(f"Z3 could not solve this instance: {reason}")
