from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Final, Generic, TypeVar, get_args, overload

from typing_extensions import Self, assert_never, override

try:
    from . import pybitwuzla
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
    from pybitwuzla import BitwuzlaTerm, Kind, Option


BZLA = pybitwuzla.Bitwuzla()
BZLA.set_option(Option.OUTPUT_NUMBER_FORMAT, "hex")
BOOL_SORT = BZLA.mk_bv_sort(1)

N = TypeVar("N", bound=int)


class Symbolic(abc.ABC):
    """
    Represents any symbolic expression. This abstract base class is inherited by
    :class:`Constraint`, :class:`Uint` and :class:`Int`.
    """

    _term: Final[BitwuzlaTerm]

    @abc.abstractmethod
    def __init__(self, term: BitwuzlaTerm, /) -> None:
        self._term = term

    @classmethod
    def _from_expr(cls, kind: Kind, *syms: Symbolic) -> Self:
        term = BZLA.mk_term(kind, tuple(s._term for s in syms))
        result = cls.__new__(cls)
        Symbolic.__init__(result, term)
        return result

    # Symbolic instances are immutable. For performance, don't copy them.
    def __copy__(self) -> Self:
        return self

    def __deepcopy__(self) -> Self:
        return self

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(`{self.smtlib()}`)"

    def smtlib(self) -> str:
        """
        Export this expression in the `SMT-LIBv2`_ format.

        .. _SMT-LIBv2: https://smtlib.cs.uiowa.edu/
        """
        if (sym := self._term.get_symbol()) is not None:
            return sym
        return self._term.dump("smt2")

    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self, /
    ) -> Constraint:
        """
        Check if this expression is equal to `other`.

        :SMT-LIB: (= self other)

        >>> Uint8(1) == Uint8(3)
        Constraint(`false`)
        """
        return Constraint._from_expr(Kind.EQUAL, self, other)

    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self, /
    ) -> Constraint:
        """
        Check if this expression is not equal to `other`.

        :SMT-LIB: (distinct self other)

        >>> Uint8(2) != Uint8(5)
        Constraint(`true`)
        """
        return Constraint._from_expr(Kind.DISTINCT, self, other)


class Constraint(Symbolic):
    """
    Represents a symbolic boolean expression. Possible concrete values are
    `True` and `False`.

    To create a :class:`Constraint` representing a concrete value, pass a
    :class:`bool` to the constructor:

    >>> Constraint(True)
    Constraint(`true`)

    To create a :class:`Constraint` representing a symbolic variable, pass a
    variable name to the constructor:

    >>> Constraint("A")
    Constraint(`A`)
    """

    def __init__(self, value: bool | str, /):
        if isinstance(value, str):
            term = BZLA.mk_const(BOOL_SORT, value)
        elif isinstance(value, bool):  # pyright: ignore[reportUnnecessaryIsInstance]
            term = BZLA.mk_bv_value(BOOL_SORT, int(value))
        else:
            assert_never(value)
        super().__init__(term)

    def __invert__(self) -> Self:
        """
        Compute the boolean NOT of this constraint.

        :SMT-LIB: (not self)

        >>> ~Constraint(True)
        Constraint(`false`)
        """
        return self._from_expr(Kind.NOT, self)

    def __and__(self, other: Self, /) -> Self:
        """
        Compute the boolean AND of this constraint with `other`.

        :SMT-LIB: (and self other)

        >>> Constraint(True) & Constraint(False)
        Constraint(`false`)
        """
        return self._from_expr(Kind.AND, self, other)

    def __or__(self, other: Self, /) -> Self:
        """
        Compute the boolean OR of this constraint with `other`.

        :SMT-LIB: (or self other)

        >>> Constraint(True) | Constraint(False)
        Constraint(`true`)
        """
        return self._from_expr(Kind.OR, self, other)

    def __xor__(self, other: Self, /) -> Self:
        """
        Compute the boolean XOR of this constraint with `other`.

        :SMT-LIB: (xor self other)

        >>> Constraint(True) ^ Constraint(False)
        Constraint(`true`)
        """
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
        """
        Perform an if-then-else based on this constraint. The result is `then`
        if the constraint evaluates to `True` and `else_` otherwise.

        :SMT-LIB: (ite self then else\\_)

        >>> Constraint(True).ite(Uint8(0xA), Uint8(0xB))
        Uint8(`#x0a`)
        """
        return then._from_expr(Kind.ITE, self, then, else_)


class BitVector(Symbolic, Generic[N]):
    """
    Represents a symbolic N-bit bitvector. This abstract base class is inherited
    by :class:`Uint` and :class:`Int`.
    """

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
        sort = BZLA.mk_bv_sort(self._width)
        if isinstance(value, str):
            term = BZLA.mk_const(sort, value)
        elif isinstance(value, int):  # pyright: ignore[reportUnnecessaryIsInstance]
            term = BZLA.mk_bv_value(sort, value)
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
        """"""
        ...

    @abc.abstractmethod
    def __le__(self, other: Self, /) -> Constraint:
        """"""
        ...

    def __invert__(self) -> Self:
        """
        Compute the bitwise NOT of this bitvector.

        :SMT-LIB: (bvnot self)

        >>> ~Uint8(7)
        Uint8(`#xf8`)
        """
        return self._from_expr(Kind.BV_NOT, self)

    def __and__(self, other: Self, /) -> Self:
        """
        Compute the bitwise AND of this bitvector with `other`.

        :SMT-LIB: (bvand self other)

        >>> Uint8(7) & Uint8(9)
        Uint8(`#x01`)
        """
        return self._from_expr(Kind.BV_AND, self, other)

    def __or__(self, other: Self, /) -> Self:
        """
        Compute the bitwise OR of this bitvector with `other`.

        :SMT-LIB: (bvor self other)

        >>> Uint8(7) | Uint8(9)
        Uint8(`#x0f`)
        """
        return self._from_expr(Kind.BV_OR, self, other)

    def __xor__(self, other: Self, /) -> Self:
        """
        Compute the bitwise XOR of this bitvector with `other`.

        :SMT-LIB: (bvxor self other)

        >>> Uint8(7) ^ Uint8(9)
        Uint8(`#x0e`)
        """
        return self._from_expr(Kind.BV_XOR, self, other)

    def __add__(self, other: Self, /) -> Self:
        """
        Compute the result of adding `other` to this bitvector.

        :SMT-LIB: (bvadd self other)

        >>> Uint8(7) + Uint8(3)
        Uint8(`#x0a`)

        >>> Int8(-1) + Int8(3)
        Int8(`#x02`)

        >>> Uint8(255) + Uint8(5)
        Uint8(`#x04`)
        """
        return self._from_expr(Kind.BV_ADD, self, other)

    def __sub__(self, other: Self, /) -> Self:
        """
        Compute the result of subtracting `other` from this bitvector.

        :SMT-LIB: (bvsub self other)

        >>> Uint8(7) - Uint8(3)
        Uint8(`#x04`)

        >>> Int8(-1) - Int8(3)
        Int8(`#xfc`)

        >>> Uint8(1) - Uint8(5)
        Uint8(`#xfc`)
        """
        return self._from_expr(Kind.BV_SUB, self, other)

    def __mul__(self, other: Self, /) -> Self:
        """
        Compute the result of multiplying this bitvector by `other`.

        :SMT-LIB: (bvmul self other)

        >>> Uint8(7) * Uint8(3)
        Uint8(`#x15`)

        >>> Int8(-1) * Int8(3)
        Int8(`#xfd`)

        >>> Uint8(16) * Uint8(23)
        Uint8(`#x70`)
        """
        return self._from_expr(Kind.BV_MUL, self, other)

    @abc.abstractmethod
    def __truediv__(self, other: Self, /) -> Self:
        ...

    @abc.abstractmethod
    def __mod__(self, other: Self, /) -> Self:
        ...

    def __lshift__(self, other: Uint[N], /) -> Self:
        """
        Compute the result of left-shifting this bitvector by `other` bits. Note
        that `other` must be a :class:`Uint`.

        :SMT-LIB: (bvshl self other)

        >>> Uint8(7) << Uint8(3)
        Uint8(`#x38`)

        >>> Int8(-1) << Int8(3)
        Int8(`#xf8`)
        """
        return self._from_expr(Kind.BV_SHL, self, other)

    @abc.abstractmethod
    def __rshift__(self, other: Uint[N], /) -> Self:
        ...


class Uint(BitVector[N]):
    """Represents an N-bit unsigned integer."""

    def __lt__(self, other: Self, /) -> Constraint:
        """
        Check if this bitvector is strictly less than `other` using an unsigned
        comparison.

        :SMT-LIB: (bvult self other)

        >>> Uint8(7) < Uint8(3)
        Constraint(`false`)
        """
        return Constraint._from_expr(Kind.BV_ULT, self, other)

    def __le__(self, other: Self, /) -> Constraint:
        """
        Check if this bitvector is less than or equal to `other` using an
        unsigned comparison.

        :SMT-LIB: (bvule self other)

        >>> Uint8(7) <= Uint8(3)
        Constraint(`false`)
        """
        return Constraint._from_expr(Kind.BV_ULE, self, other)

    def __truediv__(self, other: Self, /) -> Self:
        """
        Compute the quotient when dividing this bitvector by `other` using
        unsigned integer division.

        If the divisor is zero, the result is the bitvector of all ones.

        :SMT-LIB: (bvudiv self other)

        >>> Uint8(7) / Uint8(3)
        Uint8(`#x02`)

        >>> Uint8(7) / Uint8(0)
        Uint8(`#xff`)
        """
        return self._from_expr(Kind.BV_UDIV, self, other)

    def __mod__(self, other: Self, /) -> Self:
        """
        Compute the remainder when dividing this bitvector by `other` using
        unsigned integer division.

        If the divisor is zero, the result is the dividend.

        :SMT-LIB: (bvurem self other)

        >>> Uint8(7) % Uint8(3)
        Uint8(`#x01`)

        >>> Uint8(7) % Uint8(0)
        Uint8(`#x07`)
        """
        return self._from_expr(Kind.BV_UREM, self, other)

    def __rshift__(self, other: Uint[N], /) -> Self:
        """
        Compute the result of right-shifting this bitvector by `other` bits
        using a logical right shift.

        :SMT-LIB: (bvlshr self other)

        >>> Uint8(255) >> Uint8(2)
        Uint8(`#x3f`)
        """
        return self._from_expr(Kind.BV_SHR, self, other)


class Int(BitVector[N]):
    """Represents an N-bit signed integer in two's complement form."""

    def __lt__(self, other: Self, /) -> Constraint:
        """
        Check if this bitvector is strictly less than `other` using a signed
        comparison.

        :SMT-LIB: (bvslt self other)

        >>> Int8(-1) < Int8(3)
        Constraint(`true`)
        """
        return Constraint._from_expr(Kind.BV_SLT, self, other)

    def __le__(self, other: Self, /) -> Constraint:
        """
        Check if this bitvector is less than or equal to `other` using a signed
        comparison.

        :SMT-LIB: (bvsle self other)

        >>> Int8(-1) <= Int8(3)
        Constraint(`true`)
        """
        return Constraint._from_expr(Kind.BV_SLE, self, other)

    def __truediv__(self, other: Self, /) -> Self:
        """
        Compute the quotient when dividing this bitvector by `other` using
        signed integer division.

        If the divisor is zero, the result is `-1`.

        :SMT-LIB: (bvsdiv self other)

        >>> Int8(7) / Int8(-3)
        Int8(`#xfe`)

        >>> Int8(-7) / Int8(3)
        Int8(`#xfe`)

        >>> Int8(-7) / Int8(-3)
        Int8(`#x02`)

        >>> Int8(7) / Int8(0)
        Int8(`#xff`)
        """
        return self._from_expr(Kind.BV_SDIV, self, other)

    def __mod__(self, other: Self, /) -> Self:
        """
        Compute the remainder when dividing this bitvector by `other` using
        signed integer division.

        The sign of the remainder follows the sign of the dividend. If the
        divisor is zero, the result is the dividend.

        :SMT-LIB: (bvsrem self other)

        >>> Int8(7) % Int8(-3)
        Int8(`#x01`)

        >>> Int8(-7) % Int8(3)
        Int8(`#xff`)

        >>> Int8(-7) % Int8(-3)
        Int8(`#xff`)

        >>> Int8(7) % Int8(0)
        Int8(`#x07`)
        """
        return self._from_expr(Kind.BV_SREM, self, other)

    def __rshift__(self, other: Uint[N], /) -> Self:
        """
        Compute the result of right-shifting this bitvector by `other` bits
        using an arithmetic right shift. Note that `other` must be a
        :class:`Uint`.

        :SMT-LIB: (bvashr self other)

        >>> Int8(-8) >> Uint8(2)
        Int8(`#xfe`)
        """
        return self._from_expr(Kind.BV_ASHR, self, other)
