from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, Final, Generic, TypeVar, overload

from typing_extensions import Never, Self

from ._util import BitVectorMeta

try:
    from . import pybitwuzla
    from .pybitwuzla import BitwuzlaSort as BitwuzlaSort
    from .pybitwuzla import BitwuzlaTerm as BitwuzlaTerm
    from .pybitwuzla import Kind as Kind
    from .pybitwuzla import Option as Option
except ImportError:
    # In development, the import above will fail because pybitwuzla hasn't been
    # compiled. Fall back to the global pybitwuzla module (but don't tell the
    # typechecker, since we want it to use our local stubs).
    if TYPE_CHECKING:
        raise
    import pybitwuzla
    from pybitwuzla import BitwuzlaSort, BitwuzlaTerm, Kind, Option


BZLA = pybitwuzla.Bitwuzla()
BZLA.set_option(Option.OUTPUT_NUMBER_FORMAT, "hex")

N = TypeVar("N", bound=int)


class Symbolic(abc.ABC):
    __slots__ = ("_term",)

    @abc.abstractmethod
    def __init__(self, term: BitwuzlaTerm, /) -> None:
        self._term: Final[BitwuzlaTerm] = term

    @classmethod
    def _from_expr(cls, kind: Kind, *syms: Symbolic) -> Self:
        term = BZLA.mk_term(kind, tuple(s._term for s in syms))
        result = cls.__new__(cls)
        Symbolic.__init__(result, term)
        return result

    # Symbolic instances are immutable. For performance, don't copy them.
    def __copy__(self) -> Self:
        return self

    def __deepcopy__(self, memo: Any) -> Self:
        return self

    def __repr__(self) -> str:
        smt = self._term.get_symbol() or self._term.dump("smt2")
        return f"{self.__class__.__name__}(`{smt}`)"

    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self, /
    ) -> Constraint:
        return Constraint._from_expr(Kind.EQUAL, self, other)

    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self, /
    ) -> Constraint:
        return Constraint._from_expr(Kind.DISTINCT, self, other)


class Constraint(Symbolic):
    _sort: Final[BitwuzlaSort] = BZLA.mk_bool_sort()
    __slots__ = ()

    def __init__(self, value: bool | str, /):
        if isinstance(value, str):
            term = BZLA.mk_const(self._sort, value)
        else:
            term = BZLA.mk_bv_value(self._sort, int(value))
        super().__init__(term)

    def __invert__(self) -> Self:
        return self._from_expr(Kind.NOT, self)

    def __and__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.AND, self, other)

    def __or__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.OR, self, other)

    def __xor__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.XOR, self, other)

    def __bool__(self) -> Never:
        raise TypeError("cannot use Constraint in a boolean context")

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


class BitVector(Symbolic, Generic[N], metaclass=BitVectorMeta):
    _sort: Final[BitwuzlaSort]  # type: ignore
    __slots__ = ()

    def __init__(self, value: int | str, /) -> None:
        if isinstance(value, str):
            term = BZLA.mk_const(self._sort, value)
        else:
            term = BZLA.mk_bv_value(self._sort, value)
        super().__init__(term)

    @classmethod
    def _make_sort(cls, width: int) -> BitwuzlaSort:
        return BZLA.mk_bv_sort(width)

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
    def __truediv__(self, other: Self, /) -> Self:
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
    __slots__ = ()

    def __lt__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(Kind.BV_ULT, self, other)

    def __le__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(Kind.BV_ULE, self, other)

    def __truediv__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_UDIV, self, other)

    def __mod__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_UREM, self, other)

    def __rshift__(self, other: Uint[N], /) -> Self:
        return self._from_expr(Kind.BV_SHR, self, other)


class Int(BitVector[N]):
    __slots__ = ()

    def __lt__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(Kind.BV_SLT, self, other)

    def __le__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(Kind.BV_SLE, self, other)

    def __truediv__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_SDIV, self, other)

    def __mod__(self, other: Self, /) -> Self:
        return self._from_expr(Kind.BV_SREM, self, other)

    def __rshift__(self, other: Uint[N], /) -> Self:
        return self._from_expr(Kind.BV_ASHR, self, other)
