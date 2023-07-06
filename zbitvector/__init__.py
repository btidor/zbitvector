"""zbitvector: an efficient, well-typed interface to the Z3 and Bitwuzla SMT solvers."""

from importlib import metadata

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:
    __version__ = "dev"

from ._bitwuzla import BitVector as BitVector
from ._bitwuzla import Constraint as Constraint
from ._bitwuzla import Int as Int
from ._bitwuzla import Symbolic as Symbolic
from ._bitwuzla import Uint as Uint
