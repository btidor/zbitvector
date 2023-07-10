"""zbitvector: an efficient, well-typed interface to the Z3 and Bitwuzla SMT solvers."""

# pyright: reportUnusedImport=false

import os
from importlib import metadata
from typing import TYPE_CHECKING

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:
    __version__ = "dev"

_solver = os.getenv("ZBITVECTOR_SOLVER", "bitwuzla").lower()
if TYPE_CHECKING or _solver == "dummy":
    from . import _backend as _zbitvector
    from ._backend import BitVector as BitVector
    from ._backend import Constraint as Constraint
    from ._backend import Int as Int
    from ._backend import Symbolic as Symbolic
    from ._backend import Uint as Uint
elif _solver == "bitwuzla":
    from . import _bitwuzla as _zbitvector
    from ._bitwuzla import BitVector as BitVector
    from ._bitwuzla import Constraint as Constraint
    from ._bitwuzla import Int as Int
    from ._bitwuzla import Symbolic as Symbolic
    from ._bitwuzla import Uint as Uint
elif _solver == "z3":
    from . import _z3 as _zbitvector
    from ._z3 import BitVector as BitVector
    from ._z3 import Constraint as Constraint
    from ._z3 import Int as Int
    from ._z3 import Symbolic as Symbolic
    from ._z3 import Uint as Uint
else:
    raise ValueError(f"unknown solver: {_solver}")
