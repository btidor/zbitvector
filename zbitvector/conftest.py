from typing import Any, Dict, Literal

import pytest
from typing_extensions import TypeAlias

from . import Constraint, Int, Uint

Uint8: TypeAlias = Uint[Literal[8]]
Uint64: TypeAlias = Uint[Literal[64]]

Int8: TypeAlias = Int[Literal[8]]
Int64: TypeAlias = Int[Literal[64]]


def pytest_ignore_collect(path: Any) -> bool:
    # Don't check  _z3.py for doctests: it doesn't have any, and importing the
    # file will raise an error if Z3 isn't installed.
    if str(path).endswith("/_z3.py"):
        return True
    return False


@pytest.fixture(autouse=True)
def setup_doctest(doctest_namespace: Dict[str, Any]) -> None:
    doctest_namespace.clear
    doctest_namespace.update(
        {
            "Constraint": Constraint,
            "Uint8": Uint8,
            "Uint64": Uint64,
            "Int8": Int8,
            "Int64": Int64,
        }
    )
