from typing import Literal

from typing_extensions import TypeAlias

import zbitvector

Uint8: TypeAlias = zbitvector.Uint[Literal[8]]
Uint64: TypeAlias = zbitvector.Uint[Literal[64]]
