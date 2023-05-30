from typing import Any, Dict

import pytest

from . import Uint8


@pytest.fixture(autouse=True)
def setup_doctest(doctest_namespace: Dict[str, Any]) -> None:
    doctest_namespace["Uint8"] = Uint8
