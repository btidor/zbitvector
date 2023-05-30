from typing import Any

import pytest

import zbitvector


class Uint8(zbitvector.Uint):
    width = 8


@pytest.fixture(autouse=True)
def setup_doctest(doctest_namespace: dict[str, Any]) -> None:
    doctest_namespace["Uint8"] = Uint8
