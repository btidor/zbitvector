# pyright: reportMissingModuleSource=false
# pyright: reportUnusedImport=false

from . import pybitwuzla
from .pybitwuzla import BitwuzlaTerm, Kind, Option


class BitwuzlaContext:
    bzla: pybitwuzla.Bitwuzla
    bool_sort: pybitwuzla.BitwuzlaSort

    def __init__(self):
        self.bzla = pybitwuzla.Bitwuzla()
        self.bzla.set_option(Option.OUTPUT_NUMBER_FORMAT, "hex")
        self.bool_sort = self.bzla.mk_bv_sort(1)


ctx = BitwuzlaContext()
