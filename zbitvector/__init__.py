"""zbitvector: an efficient, well-typed interface to the Z3 and Bitwuzla SMT solvers."""

from .bitvector import Int as Int
from .bitvector import Uint as Uint
from .constraint import Constraint as Constraint

from importlib import metadata

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:
    __version__ = "dev"
