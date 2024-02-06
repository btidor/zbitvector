"""Backend implementation for the Bitwuzla solver."""

from __future__ import annotations

import abc
import os
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Final,
    Generic,
    List,
    Tuple,
    TypeVar,
    Union,
)

from typing_extensions import Never, Self

from ._util import ArrayMeta, BitVectorMeta

try:
    from . import pybitwuzla
    from .pybitwuzla import BitwuzlaSort as BitwuzlaSort
    from .pybitwuzla import BitwuzlaTerm as BitwuzlaTerm
    from .pybitwuzla import Kind as Kind
    from .pybitwuzla import Option as Option
    from .pybitwuzla import Result as Result
except ImportError:
    # In development, the import above will fail because pybitwuzla hasn't been
    # compiled. Fall back to the global pybitwuzla module (but don't tell the
    # typechecker, since we want it to use our local stubs).
    if TYPE_CHECKING:
        raise
    import pybitwuzla
    from pybitwuzla import BitwuzlaSort, BitwuzlaTerm, Kind, Option, Result


N = TypeVar("N", bound=int)
M = TypeVar("M", bound=int)

BZLA = pybitwuzla.Bitwuzla()
BZLA.set_option(Option.INCREMENTAL, True)
BZLA.set_option(Option.PRODUCE_MODELS, True)
BZLA.set_option(Option.OUTPUT_NUMBER_FORMAT, "hex")

OPTIMIZE = os.getenv("ZBITVECTOR_OPTIMIZE", "0").lower() in ("true", "t", "1")

# We have to use a single, global Bitwuzla instance because all terms are
# associated with an instance and can't be transferred to another. Therefore, we
# track whether the last call to `check_sat()` was UNSAT (False) or SAT (the
# Solver responsible for the call, if available, or True otherwise).
last_check: Solver | bool = False


CACHE: Dict[str, Tuple[type, BitwuzlaTerm]] = {}


def _mk_const(instance: Symbolic | Array[K, V], name: str) -> BitwuzlaTerm:
    # If we call `mk_const` twice with the same name, Bitwuzla will create two
    # independent-but-indistinguishable constants. To avoid confusion and
    # maintain parity with Z3, we cache constants by name.
    if name not in CACHE:
        term = BZLA.mk_const(instance._sort, name)  # pyright: ignore[reportPrivateUsage]
        CACHE[name] = (instance.__class__, term)
    cls, term = CACHE[name]
    if not isinstance(instance, cls):
        raise ValueError(
            f'cannot create {instance.__class__.__name__}("{name}") '
            f'because {cls.__name__}("{name}") already exists'
        )
    return term


def _reset_solver() -> None:
    global last_check
    if last_check is False:
        assert BZLA.check_sat() == Result.SAT
        last_check = True


class Symbolic(abc.ABC):
    _sort: ClassVar[BitwuzlaSort]
    __slots__ = ("_term",)

    @abc.abstractmethod
    def __init__(self, term: BitwuzlaTerm, /) -> None:
        self._term: BitwuzlaTerm = term

    @classmethod
    def _from_expr(cls, kind: Kind, *syms: Symbolic | Array[K, V]) -> Self:
        term = BZLA.mk_term(
            kind,
            tuple(s._term for s in syms),  # pyright: ignore[reportPrivateUsage]
        )
        result = cls.__new__(cls)
        Symbolic.__init__(result, term)
        return result

    @abc.abstractmethod
    def _evaluate(self) -> bool | int:
        ...

    def __copy__(self) -> Self:
        return self

    def __deepcopy__(self, memo: Any, /) -> Self:
        return self

    def __repr__(self) -> str:
        if (sym := self._term.get_symbol()) is not None:
            r = sym
        else:
            r = self._term.dump("smt2")
        return f"{self.__class__.__name__}(`{r}`)"

    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self, /
    ) -> Constraint:
        return Constraint._from_expr(Kind.EQUAL, self, other)

    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self, /
    ) -> Constraint:
        return Constraint._from_expr(Kind.DISTINCT, self, other)

    def __hash__(self) -> int:
        return self._term.__hash__()

    def reveal(self) -> bool | int | None:
        if not self._term.is_bv_value():
            return None
        _reset_solver()
        return self._evaluate()


class Constraint(Symbolic):
    _sort: ClassVar[BitwuzlaSort] = BZLA.mk_bool_sort()
    __slots__ = ()

    def __init__(self, value: bool | str, /):
        if isinstance(value, str):
            term = _mk_const(self, value)
        else:
            term = BZLA.mk_bv_value(self._sort, int(value))
        super().__init__(term)

    def _evaluate(self) -> bool:
        return bool(int(BZLA.get_value_str(self._term), 2))

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

    def ite(self, then: Symbolic, else_: Symbolic, /) -> Symbolic:
        return then._from_expr(Kind.ITE, self, then, else_)


class BitVector(Symbolic, Generic[N], metaclass=BitVectorMeta):
    width: Final[int]  # type: ignore
    _sort: ClassVar[BitwuzlaSort]
    __slots__ = ()

    def __init__(self, value: int | str, /) -> None:
        if isinstance(value, str):
            term = _mk_const(self, value)
        else:
            term = BZLA.mk_bv_value(self._sort, value)
        super().__init__(term)

    @classmethod
    def _make_sort(cls, width: int) -> BitwuzlaSort:
        return BZLA.mk_bv_sort(width)

    def _from_expr1(
        self, other: type[BitVector[M]], kind: Kind | None, args: tuple[int, ...]
    ) -> BitVector[M]:
        if kind is None:
            term = self._term
        else:
            term = Optimizations.raise_ite(
                self._term, lambda t: BZLA.mk_term(kind, (t,), args)
            )
        result = other.__new__(other)
        Symbolic.__init__(result, term)
        return result

    def _from_expr2(self, kind: Kind, other: Symbolic) -> Self:
        term = Optimizations.raise_ite(
            self._term,
            lambda t: Optimizations.stack_shifts(kind, self.width, t, other._term),
        )
        result = self.__class__.__new__(self.__class__)
        Symbolic.__init__(result, term)
        return result

    def _from_expr3(self, other: type[BitVector[M]]) -> BitVector[M]:
        term = Optimizations.raise_ite(
            self._term,
            lambda t: Optimizations.rewrite_extract_shift(t, self.width, other.width),
        )
        result = other.__new__(other)
        Symbolic.__init__(result, term)
        return result

    @abc.abstractmethod
    def __lt__(self, other: Self, /) -> Constraint:
        ...

    @abc.abstractmethod
    def __le__(self, other: Self, /) -> Constraint:
        ...

    def __invert__(self) -> Self:
        return self._from_expr(Kind.BV_NOT, self)

    def __and__(self, other: Self, /) -> Self:
        return self._from_expr2(Kind.BV_AND, other)

    def __or__(self, other: Self, /) -> Self:
        return self._from_expr2(Kind.BV_OR, other)

    def __xor__(self, other: Self, /) -> Self:
        return self._from_expr2(Kind.BV_XOR, other)

    def __add__(self, other: Self, /) -> Self:
        return self._from_expr2(Kind.BV_ADD, other)

    def __sub__(self, other: Self, /) -> Self:
        return self._from_expr2(Kind.BV_SUB, other)

    def __mul__(self, other: Self, /) -> Self:
        return self._from_expr2(Kind.BV_MUL, other)

    @abc.abstractmethod
    def __truediv__(self, other: Self, /) -> Self:
        ...

    @abc.abstractmethod
    def __mod__(self, other: Self, /) -> Self:
        ...

    def __lshift__(self, other: Uint[N], /) -> Self:
        return self._from_expr2(Kind.BV_SHL, other)

    @abc.abstractmethod
    def __rshift__(self, other: Uint[N], /) -> Self:
        ...


class Uint(BitVector[N]):
    __slots__ = ()

    def _evaluate(self) -> int:
        return int(BZLA.get_value_str(self._term), 2)

    def __lt__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(Kind.BV_ULT, self, other)

    def __le__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(Kind.BV_ULE, self, other)

    def __truediv__(self, other: Self, /) -> Self:
        return self._from_expr2(Kind.BV_UDIV, other)

    def __mod__(self, other: Self, /) -> Self:
        return self._from_expr2(Kind.BV_UREM, other)

    def __rshift__(self, other: Uint[N], /) -> Self:
        return self._from_expr2(Kind.BV_SHR, other)

    def into(self, other: type[BitVector[M]], /) -> BitVector[M]:
        if self.width < other.width:
            return self._from_expr1(
                other, Kind.BV_ZERO_EXTEND, (other.width - self.width,)
            )
        elif self.width > other.width:
            return self._from_expr3(other)
        else:
            return self._from_expr1(other, None, ())


class Int(BitVector[N]):
    __slots__ = ()

    def _evaluate(self) -> int:
        i = int(BZLA.get_value_str(self._term), 2)
        if i & (1 << (self.width - 1)) == 0:
            return i
        return i - (1 << self.width)

    def __lt__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(Kind.BV_SLT, self, other)

    def __le__(self, other: Self, /) -> Constraint:
        return Constraint._from_expr(Kind.BV_SLE, self, other)

    def __truediv__(self, other: Self, /) -> Self:
        return self._from_expr2(Kind.BV_SDIV, other)

    def __mod__(self, other: Self, /) -> Self:
        return self._from_expr2(Kind.BV_SREM, other)

    def __rshift__(self, other: Uint[N], /) -> Self:
        return self._from_expr2(Kind.BV_ASHR, other)

    def into(self, other: type[BitVector[M]], /) -> BitVector[M]:
        if self.width < other.width:
            return self._from_expr1(
                other, Kind.BV_SIGN_EXTEND, (other.width - self.width,)
            )
        elif self.width > other.width:
            return self._from_expr3(other)
        else:
            return self._from_expr1(other, None, ())


K = TypeVar("K", bound=Union[Uint[Any], Int[Any]])
V = TypeVar("V", bound=Union[Uint[Any], Int[Any]])


class Array(Generic[K, V], metaclass=ArrayMeta):
    _key: type[K]
    _value: type[V]
    _sort: ClassVar[BitwuzlaSort]
    __slots__ = ("_term",)

    def __init__(self, value: V | str, /) -> None:
        if isinstance(value, str):
            term = _mk_const(self, value)
        else:
            term = BZLA.mk_const_array(self._sort, value._term)  # pyright: ignore[reportPrivateUsage]
        self._term: BitwuzlaTerm = term

    @classmethod
    def _make_sort(cls, key: K, value: V) -> BitwuzlaSort:
        return BZLA.mk_array_sort(key._sort, value._sort)  # pyright: ignore[reportPrivateUsage]

    def __copy__(self) -> Self:
        result = self.__new__(self.__class__)
        result._term = self._term
        return result

    def __deepcopy__(self, memo: Any, /) -> Self:
        return self.__copy__()

    def __repr__(self) -> str:
        if (sym := self._term.get_symbol()) is not None:
            r = sym
        elif self._term.is_const_array():
            r = self._term.get_children()[0].dump("smt2")
        else:
            r = self._term.dump("smt2")
        return f"{self.__class__.__name__}(`{r}`)"

    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Never, /
    ) -> Never:
        raise TypeError("arrays cannot be compared for equality.")

    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Never, /
    ) -> Never:
        raise TypeError("arrays cannot be compared for equality.")

    def __getitem__(self, key: K) -> V:
        return self._value._from_expr(  # pyright: ignore[reportPrivateUsage]
            Kind.ARRAY_SELECT, self, key
        )

    def __setitem__(self, key: K, value: V) -> None:
        self._term = BZLA.mk_term(
            Kind.ARRAY_STORE,
            (self._term, key._term, value._term),  # pyright: ignore[reportPrivateUsage]
        )


class Solver:
    __slots__ = ("_assertions", "_current")

    def __init__(self) -> None:
        self._assertions: List[Constraint] = []
        self._current = False

    def add(self, assertion: Constraint, /) -> None:
        self._assertions.append(assertion)
        self._current = False

    def check(self, *assumptions: Constraint) -> bool:
        # Unfortunately, we have only the single global solver instance, BZLA,
        # because all terms are tied to it. This means we can't build up
        # assumptions using `assert_formula`. Instead, assume them all on every
        # call to `check`:
        global last_check
        self._current, last_check = False, False

        for c in self._assertions:
            BZLA.assume_formula(c._term)  # pyright: ignore[reportPrivateUsage]
        for c in assumptions:
            BZLA.assume_formula(c._term)  # pyright: ignore[reportPrivateUsage]

        r = BZLA.check_sat()
        if r == Result.SAT:
            self._current, last_check = True, self
            return True
        elif r == Result.UNSAT:
            return False
        else:
            raise RuntimeError("Bitwuzla could not solve this instance")

    def evaluate(self, bv: BitVector[N], /) -> int:
        global last_check
        if not self._current or last_check is not self:
            raise ValueError("solver is not ready for model evaluation.")
        return bv._evaluate()  # pyright: ignore[reportPrivateUsage]


class Optimizations:
    @classmethod
    def raise_ite(
        cls, term: BitwuzlaTerm, op: Callable[[BitwuzlaTerm], BitwuzlaTerm]
    ) -> BitwuzlaTerm:
        if not OPTIMIZE or term.get_kind() != Kind.ITE:
            return op(term)
        cond, term1, term2 = term.get_children()
        return BZLA.mk_term(Kind.ITE, (cond, op(term1), op(term2)))

    @classmethod
    def stack_shifts(
        cls, kind: Kind, width: int, term1: BitwuzlaTerm, term2: BitwuzlaTerm
    ) -> BitwuzlaTerm:
        if (
            not OPTIMIZE
            or kind not in (Kind.BV_SHL, Kind.BV_SHR)
            or term1.get_kind() != kind
            or not term2.is_bv_value()
        ):
            return BZLA.mk_term(kind, (term1, term2))
        (base, a) = term1.get_children()
        if not a.is_bv_value():
            return BZLA.mk_term(kind, (term1, term2))

        _reset_solver()
        shift = int(BZLA.get_value_str(term2), 2) + int(BZLA.get_value_str(a), 2)
        if shift > width:
            return BZLA.mk_bv_value(term1.get_sort(), 0)  # unsigned shifts only!
        shift = BZLA.mk_bv_value(term1.get_sort(), shift)
        return BZLA.mk_term(kind, (base, shift))

    @classmethod
    def rewrite_extract_shift(
        cls, term: BitwuzlaTerm, width: int, bits: int
    ) -> BitwuzlaTerm:
        if not OPTIMIZE or (kind := term.get_kind()) not in (
            Kind.BV_SHL,
            Kind.BV_SHR,
        ):
            return BZLA.mk_term(Kind.BV_EXTRACT, (term,), (bits - 1, 0))

        (base, shift) = term.get_children()
        if not shift.is_bv_value():
            return BZLA.mk_term(Kind.BV_EXTRACT, (term,), (bits - 1, 0))

        _reset_solver()
        high, low, shift = bits - 1, 0, int(BZLA.get_value_str(shift), 2)
        if kind == Kind.BV_SHL:
            if shift >= bits:
                return BZLA.mk_bv_value(BZLA.mk_bv_sort(bits), 0)
        else:
            if shift >= width:
                return BZLA.mk_bv_value(BZLA.mk_bv_sort(bits), 0)
            elif bits + shift - 1 < width:
                high, low, term = high + shift, low + shift, base
        return BZLA.mk_term(Kind.BV_EXTRACT, (term,), (high, low))
