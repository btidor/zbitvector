import typing

try:
    from . import pybitwuzla
    from .pybitwuzla import BitwuzlaTerm as BitwuzlaTerm
    from .pybitwuzla import Kind as Kind
    from .pybitwuzla import Option as Option
except ImportError:
    # In development, the import above will fail because pybitwuzla hasn't been
    # compiled. Fall back to the global pybitwuzla module (but don't tell the
    # typechecker, since we want it to use our local stubs).
    if typing.TYPE_CHECKING:
        raise
    import pybitwuzla
    from pybitwuzla import BitwuzlaTerm, Kind, Option


class BitwuzlaContext:
    bzla: pybitwuzla.Bitwuzla
    bool_sort: pybitwuzla.BitwuzlaSort

    def __init__(self):
        self.bzla = pybitwuzla.Bitwuzla()
        self.bzla.set_option(Option.OUTPUT_NUMBER_FORMAT, "hex")
        self.bool_sort = self.bzla.mk_bv_sort(1)


ctx = BitwuzlaContext()
