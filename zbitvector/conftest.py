from typing import Any, Dict, Literal

import pytest
from typing_extensions import TypeAlias

from . import bitvector

Uint8: TypeAlias = bitvector.Uint[Literal[8]]
Uint64: TypeAlias = bitvector.Uint[Literal[64]]


@pytest.fixture(autouse=True)
def setup_doctest(doctest_namespace: Dict[str, Any]) -> None:
    doctest_namespace["Uint8"] = Uint8
