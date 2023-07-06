"""zbitvector: an efficient, well-typed interface to the Z3 and Bitwuzla SMT solvers."""


from importlib import metadata
from typing import TYPE_CHECKING

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:
    __version__ = "dev"

# pyright: reportUnusedImport=false

if TYPE_CHECKING:
    from ._backend import BitVector, Constraint, Int, Symbolic, Uint
else:
    from ._bitwuzla import BitVector, Constraint, Int, Symbolic, Uint
