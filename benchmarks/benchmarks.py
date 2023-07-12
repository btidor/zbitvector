from typing import Literal

from pympler.asizeof import asizeof  # type: ignore
from typing_extensions import TypeAlias

from zbitvector import Constraint, Int, Uint

# pyright: reportUnusedExpression=false

Uint64: TypeAlias = Uint[Literal[64]]
Int64: TypeAlias = Int[Literal[64]]


class TimeConstraintSuite:
    def track_size(self):
        return asizeof(Constraint(True))

    def time_create(self):
        for _ in range(500):
            Constraint(True)
            Constraint(False)

    def time_boolean(self):
        for _ in range(200):
            ~Constraint(True)
            Constraint(True) & Constraint(False)
            Constraint(True) | Constraint(True)
            Constraint(False) ^ Constraint(False)
            Constraint(True).ite(Constraint(False), Constraint(True))


class TimeUintSuite:
    def track_size(self):
        return asizeof(Uint64(0))

    def time_create(self):
        for i in range(1000):
            Uint64(i)

    def time_boolean(self):
        for i in range(166):
            ~Uint64(i)
            Uint64(1000 + i) & Uint64(2000 + i)
            Uint64(3000 + i) | Uint64(4000 + i)
            Uint64(5000 + i) ^ Uint64(6000 + i)
            Uint64(7000 + i) << Uint64(i % 64)
            Uint64(8000 + i) >> Uint64(i % 64)

    def time_arithmetic(self):
        for i in range(200):
            Uint64(3 * i) + Uint64(5 * i)
            Uint64(7 * i) - Uint64(11 * i)
            Uint64(13 * i) * Uint64(17 * i)
            Uint64(19 * i) / Uint64(i + 6)
            Uint64(23 * i) % Uint64(i + 16)


class IntSuite:
    def track_size(self):
        return asizeof(Int64(0))

    def time_create(self):
        for i in range(1000):
            Int64(i)

    def time_boolean(self):
        for i in range(166):
            ~Int64(i)
            Int64(1000 + i) & Int64(2000 + i)
            Int64(3000 + i) | Int64(4000 + i)
            Int64(5000 + i) ^ Int64(6000 + i)
            Int64(7000 + i) << Uint64(i % 64)
            Int64(8000 + i) >> Uint64(i % 64)

    def time_arithmetic(self):
        for i in range(200):
            Int64(3 * i) + Int64(5 * i)
            Int64(7 * i) - Int64(11 * i)
            Int64(13 * i) * Int64(17 * i)
            Int64(19 * i) / Int64(i + 6)
            Int64(23 * i) % Int64(i + 16)
