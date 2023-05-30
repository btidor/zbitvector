import abc
from typing import Final

from typing_extensions import Self

from ._bitwuzla import BitwuzlaTerm, Kind, ctx


class Symbolic(abc.ABC):
    _term: Final[BitwuzlaTerm]

    @abc.abstractmethod
    def __init__(self, term: BitwuzlaTerm) -> None:
        self._term = term

    @classmethod
    def from_expr(cls, kind: Kind, *terms: BitwuzlaTerm) -> Self:
        term = ctx.bzla.mk_term(kind, terms, [])
        result = cls.__new__(cls)
        Symbolic.__init__(result, term)
        return result

    def __copy__(self) -> Self:
        return self

    def __deepcopy__(self) -> Self:
        return self

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.TODO"

    def smtlib(self) -> str:
        return self._term.dump("smt2")
