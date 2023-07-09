from __future__ import annotations

import abc
from typing import Any, Generic, TypeVar, overload

from typing_extensions import Self, override

N = TypeVar("N", bound=int)


class Symbolic(abc.ABC):
    """
    Represents any symbolic expression. This abstract base class is inherited by
    :class:`Constraint`, :class:`Uint` and :class:`Int`.
    """

    @abc.abstractmethod
    def __init__(self, term: Any, /) -> None:
        raise NotImplementedError

    def __copy__(self) -> Self:
        raise NotImplementedError

    def __deepcopy__(self) -> Self:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def smtlib(self) -> str:
        """
        Export this expression in the `SMT-LIBv2`_ format.

        .. _SMT-LIBv2: https://smtlib.cs.uiowa.edu/
        """
        raise NotImplementedError

    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self, /
    ) -> Constraint:
        """
        Check if this expression is equal to `other`.

        :SMT-LIB: (= self other)

        >>> Uint8(1) == Uint8(3)
        Constraint(`false`)
        """
        raise NotImplementedError

    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Self, /
    ) -> Constraint:
        """
        Check if this expression is not equal to `other`.

        :SMT-LIB: (distinct self other)

        >>> Uint8(2) != Uint8(5)
        Constraint(`true`)
        """
        raise NotImplementedError


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
        raise NotImplementedError

    def __invert__(self) -> Self:
        """
        Compute the boolean NOT of this constraint.

        :SMT-LIB: (not self)

        >>> ~Constraint(True)
        Constraint(`false`)
        """
        raise NotImplementedError

    def __and__(self, other: Self, /) -> Self:
        """
        Compute the boolean AND of this constraint with `other`.

        :SMT-LIB: (and self other)

        >>> Constraint(True) & Constraint(False)
        Constraint(`false`)
        """
        raise NotImplementedError

    def __or__(self, other: Self, /) -> Self:
        """
        Compute the boolean OR of this constraint with `other`.

        :SMT-LIB: (or self other)

        >>> Constraint(True) | Constraint(False)
        Constraint(`true`)
        """
        raise NotImplementedError

    def __xor__(self, other: Self, /) -> Self:
        """
        Compute the boolean XOR of this constraint with `other`.

        :SMT-LIB: (xor self other)

        >>> Constraint(True) ^ Constraint(False)
        Constraint(`true`)
        """
        raise NotImplementedError

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
        raise NotImplementedError


class BitVector(Symbolic, Generic[N]):
    """
    Represents a symbolic N-bit bitvector. This abstract base class is inherited
    by :class:`Uint` and :class:`Int`.
    """

    def __init__(self, value: int | str, /) -> None:
        raise NotImplementedError

    @override
    def __repr__(self) -> str:
        raise NotImplementedError

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
        raise NotImplementedError

    def __and__(self, other: Self, /) -> Self:
        """
        Compute the bitwise AND of this bitvector with `other`.

        :SMT-LIB: (bvand self other)

        >>> Uint8(7) & Uint8(9)
        Uint8(`#x01`)
        """
        raise NotImplementedError

    def __or__(self, other: Self, /) -> Self:
        """
        Compute the bitwise OR of this bitvector with `other`.

        :SMT-LIB: (bvor self other)

        >>> Uint8(7) | Uint8(9)
        Uint8(`#x0f`)
        """
        raise NotImplementedError

    def __xor__(self, other: Self, /) -> Self:
        """
        Compute the bitwise XOR of this bitvector with `other`.

        :SMT-LIB: (bvxor self other)

        >>> Uint8(7) ^ Uint8(9)
        Uint8(`#x0e`)
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def __le__(self, other: Self, /) -> Constraint:
        """
        Check if this bitvector is less than or equal to `other` using an
        unsigned comparison.

        :SMT-LIB: (bvule self other)

        >>> Uint8(7) <= Uint8(3)
        Constraint(`false`)
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def __rshift__(self, other: Uint[N], /) -> Self:
        """
        Compute the result of right-shifting this bitvector by `other` bits
        using a logical right shift.

        :SMT-LIB: (bvlshr self other)

        >>> Uint8(255) >> Uint8(2)
        Uint8(`#x3f`)
        """
        raise NotImplementedError


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
        raise NotImplementedError

    def __le__(self, other: Self, /) -> Constraint:
        """
        Check if this bitvector is less than or equal to `other` using a signed
        comparison.

        :SMT-LIB: (bvsle self other)

        >>> Int8(-1) <= Int8(3)
        Constraint(`true`)
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def __rshift__(self, other: Uint[N], /) -> Self:
        """
        Compute the result of right-shifting this bitvector by `other` bits
        using an arithmetic right shift. Note that `other` must be a
        :class:`Uint`.

        :SMT-LIB: (bvashr self other)

        >>> Int8(-8) >> Uint8(2)
        Int8(`#xfe`)
        """
        raise NotImplementedError