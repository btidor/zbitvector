from __future__ import annotations

from typing import TypeVar

from ._bitwuzla import Kind, ctx
from .symbolic import Symbolic

S = TypeVar("S", bound=Symbolic)


class Constraint(Symbolic):
    def __init__(self, value: bool | str):
        match value:
            case str():
                term = ctx.bzla.mk_const(ctx.bool_sort, value)
            case bool():
                term = ctx.bzla.mk_bv_value(ctx.bool_sort, value)
        super().__init__(term)

    def __invert__(self) -> Constraint:
        return self.from_expr(Kind.NOT, self._term)

    def ite(self, then: S, else_: S) -> S:
        return then.from_expr(Kind.ITE, self._term, then._term, else_._term)
