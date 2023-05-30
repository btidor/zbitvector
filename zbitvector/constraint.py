from __future__ import annotations

from typing import TypeVar
from typing_extensions import assert_never

from ._bitwuzla import Kind, ctx
from .symbolic import Symbolic

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
