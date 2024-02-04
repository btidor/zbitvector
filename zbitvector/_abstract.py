"""
Abstract solver backend.

For specific implementations, see _bitwuzla.py and _z3.py.
"""

from __future__ import annotations

import abc
from typing import Any, ClassVar, Final, Generic, TypeVar, Union, overload

from typing_extensions import Never, Self

N = TypeVar("N", bound=int)
M = TypeVar("M", bound=int)


class Symbolic(abc.ABC):
    """
    represents an immutable symbolic value. This abstract base class is
    inherited by :class:`Constraint`, :class:`Uint` and :class:`Int`.
    """

    @abc.abstractmethod
    def __init__(self, term: Any, /) -> None:
        raise NotImplementedError

    # Implementation Note: Symbolic instances are immutable. For performance,
    # don't copy them.
    def __copy__(self) -> Self:
        raise NotImplementedError

    def __deepcopy__(self, memo: Any, /) -> Self:
        raise NotImplementedError

    def __repr__(self) -> str:
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

    def __hash__(self) -> int:
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

    >>> Constraint("C")
    Constraint(`C`)
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

    def __bool__(self) -> Never:
        """
        Prohibit using :class:`Constraint` in a boolean context.

        Without this check, all instances of :class:`Constraint` would be
        considered true and it would be easy to mis-use :class:`Constraint` in
        an if statement:

        .. code::

            a, b = Uint8(...), Uint8(...)
            if a > b:
                ...
            else:
                ...  # unreachable!
        """
        raise NotImplementedError

    @overload
    def ite(self, then: Uint[N], else_: Uint[N], /) -> Uint[N]:
        ...

    @overload
    def ite(self, then: Int[N], else_: Int[N], /) -> Int[N]:
        ...

    @overload
    def ite(self, then: Constraint, else_: Constraint, /) -> Constraint:
        ...

    def ite(self, then: Symbolic, else_: Symbolic, /) -> Symbolic:
        r"""
        Perform an if-then-else based on this constraint. The result is `then`
        if the constraint evaluates to `True` and `else_` otherwise.

        :SMT-LIB: (ite self then else\_)

        >>> Constraint(True).ite(Uint8(0xA), Uint8(0xB))
        Uint8(`#x0a`)
        """
        raise NotImplementedError

    def reveal(self) -> bool | None:
        """
        Reveal the simplified value of this constraint *without* invoking the
        solver. If the constraint does not simplify to a constant literal,
        returns `None`.

        >>> (Constraint("C") | Constraint(True)).reveal()
        True

        >>> (Constraint("C") | Constraint(False)).reveal() is None
        True
        """
        raise NotImplementedError


class BitVector(Symbolic, Generic[N]):
    """
    Represents a symbolic N-bit bitvector. This abstract base class is inherited
    by :class:`Uint` and :class:`Int`.

    :SMT-LIB: `theory of fixed-sized bitvectors`

    To create a :class:`BitVector` representing a concrete value, pass an
    :class:`int` to the constructor:

    >>> Uint8(0)
    Uint8(`#x00`)

    To create a :class:`BitVector` representing a symbolic variable, pass a
    variable name to the constructor:

    >>> Int8("I")
    Int8(`I`)
    """

    width: Final[int]  # type: ignore
    """
    The number of bits in this bitvector.

    >>> Uint8(0).width
    8
    """

    def __init__(self, value: int | str, /) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __lt__(self, other: Self, /) -> Constraint:
        ...

    @abc.abstractmethod
    def __le__(self, other: Self, /) -> Constraint:
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

    @overload
    def into(self: Uint[N], other: type[Int[N]], /) -> Int[N]:
        ...

    @overload
    def into(self: Uint[N], other: type[Uint[M]], /) -> Uint[M]:
        ...

    def into(self, other: type[BitVector[M]], /) -> BitVector[M]:
        """
        Forcibly convert this bitvector to the given type.

        When converting to an :class:`Int`, the underlying bits are
        reinterpreted as a two's complement signed integer:

        >>> Uint8(255).into(Int8)
        Int8(`#xff`)

        When converting to a longer :class:`Uint`, the underling bits are
        zero-extended:

        >>> Uint8(0xFF).into(Uint64)
        Uint64(`#x00000000000000ff`)

        When converting to a shorter :class:`Uint`, the underlying bits are
        truncated:

        >>> Uint64(0x1234).into(Uint8)
        Uint8(`#x34`)
        """
        raise NotImplementedError

    def reveal(self) -> int | None:
        """
        Reveal the simplified value of this constraint *without* invoking the
        solver. If the constraint does not simplify to a constant literal,
        returns `None`.

        >>> (Uint8(2) + Uint8(3)).reveal()
        5

        >>> (Uint8("X") + Uint8(1)).reveal() is None
        True
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

    @overload
    def into(self: Int[N], other: type[Uint[N]], /) -> Uint[N]:
        ...

    @overload
    def into(self: Int[N], other: type[Int[M]], /) -> Int[M]:
        ...

    def into(self, other: type[BitVector[M]], /) -> BitVector[M]:
        """
        Forcibly convert this bitvector to the given type.

        When converting to a :class:`Uint`, the underlying bits are
        reinterpreted as an unsigned integer, from two's complement form:

        >>> Int8(-1).into(Uint8)
        Uint8(`#xff`)

        When converting to a longer :class:`Int`, the underling bits are
        sign-extended:

        >>> Int8(0xFF).into(Int64)
        Int64(`#xffffffffffffffff`)

        When converting to a shorter :class:`Int`, the underlying bits are
        truncated:

        >>> Int64(0xFFFFFFFFFFFFFF01).into(Int8)
        Int8(`#x01`)
        """
        raise NotImplementedError

    def reveal(self) -> int | None:
        """
        Reveal the simplified value of this constraint *without* invoking the
        solver. If the constraint does not simplify to a constant literal,
        returns `None`.

        >>> (Int8(2) - Int8(3)).reveal()
        -1

        >>> (Int8("Y") + Int8(1)).reveal() is None
        True
        """
        raise NotImplementedError


K = TypeVar("K", bound=Union[Uint[Any], Int[Any]])
V = TypeVar("V", bound=Union[Uint[Any], Int[Any]])


class Array(Generic[K, V]):
    """
    Represents a mutable symbolic array mapping a :class:`BitVector` to a
    :class:`BitVector`. Arrays do not have a length: they map the full domain to
    the full range.

    :SMT-LIB: `theory of functional arrays`

    To create an :class:`Array` where all keys map to a single default value,
    pass a :class:`BitVector` to the constructor:

    >>> Array[Uint8, Uint64](Uint64(0))
    Array[Uint8, Uint64](`#x0000000000000000`)

    To create a fully unconstrained :class:`Array`, pass a variable name to the
    constructor:

    >>> Array[Int8, Int64]("A")
    Array[Int8, Int64](`A`)
    """

    __hash__: ClassVar[None] = None  # pyright: ignore[reportIncompatibleMethodOverride]

    def __init__(self, value: V | str, /) -> None:
        raise NotImplementedError

    def __copy__(self) -> Self:
        raise NotImplementedError

    def __deepcopy__(self, memo: Any, /) -> Self:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    # Implementation Note: Arrays cannot be compared for equality.
    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Never, /
    ) -> Never:
        raise NotImplementedError

    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Never, /
    ) -> Never:
        raise NotImplementedError

    def __getitem__(self, key: K) -> V:
        """
        Look up the item at index `key`.

        :SMT-LIB: (select self key)

        >>> A = Array[Uint8, Uint64](Uint64(0))
        >>> A[Uint8(100)]
        Uint64(`#x0000000000000000`)
        """
        raise NotImplementedError

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set the item at index `key` to `value`.

        :SMT-LIB: (store self key value)

        >>> A = Array[Uint8, Uint64](Uint64(0))
        >>> A[Uint8(1)] = Uint64(0x1234)
        >>> A[Uint8(1)]
        Uint64(`#x0000000000001234`)
        """
        raise NotImplementedError


class Solver:
    """
    A SAT solver instance.

    >>> s = Solver()
    >>> s.add(Uint8("B") == Uint8(1))
    >>> s.check()
    True
    >>> s.evaluate(Uint8("B"))
    1
    >>> s.add(Uint8("B") == Uint8(2))
    >>> s.check()
    False
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def add(self, assertion: Constraint, /) -> None:
        """Permanently add an assertion to the solver state."""
        raise NotImplementedError

    def check(self, *assumptions: Constraint) -> bool:
        """
        Check whether the solver state is satisfiable.

        If provided, *assumptions* are temporarily added to the solver state for
        this check only.
        """
        raise NotImplementedError

    def evaluate(self, bv: BitVector[N], /) -> int:
        """
        Return a value for the given :class:`BitVector` consistent with the
        solver's model.

        Raises a :class:`ValueError` if these preconditions are not met:
         - The most recent call to :func:`check` returned `True`.
         - No subsequent calls to :func:`add` have been made.
         - With the Bitwuzla backend: no subsequent calls to :func:`check` have
           been made with any other :class:`Solver` instance.
        """
        raise NotImplementedError
