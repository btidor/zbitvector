"""zbitvector: an efficient, well-typed interface to the Z3 and Bitwuzla SMT solvers."""

import os
from importlib import metadata
from typing import TYPE_CHECKING

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:
    __version__ = "dev"


__all__ = ("BitVector", "Constraint", "Int", "Symbolic", "Uint")


_solver = os.getenv("ZBITVECTOR_SOLVER", "bitwuzla").lower()

if _solver == "dummy":
    from . import _abstract as _backend
elif _solver == "bitwuzla":
    from . import _bitwuzla as _backend
elif _solver == "z3":
    from . import _z3 as _backend
else:
    raise ValueError(f"unknown solver: {_solver}")

if TYPE_CHECKING:
    # Make imports explicit for the type checker.
    from ._abstract import BitVector as BitVector
    from ._abstract import Constraint as Constraint
    from ._abstract import Int as Int
    from ._abstract import Symbolic as Symbolic
    from ._abstract import Uint as Uint
else:
    for _name in __all__:
        _member = getattr(_backend, _name)
        _member.__module__ = __name__
        globals()[_name] = _member
