#!/usr/bin/env pytest

from __future__ import annotations

import inspect
from types import ModuleType

import zbitvector._abstract


def test_abstract():
    """Test that the current zbitvector backend matches the abstract spec."""
    assert _enumerate_module(zbitvector._abstract) == _enumerate_module(zbitvector)


def _enumerate_module(module: ModuleType) -> set[str]:
    results: set[str] = set()
    for name in zbitvector.__all__:
        c = getattr(module, name)
        for _, f in inspect.getmembers(c):
            if not inspect.isfunction(f):
                continue
            if f.__name__.startswith("_") and not f.__name__.startswith("__"):
                # Skip private members
                continue
            if c.__name__ == "Symbolic" and f.__name__ == "__init__":
                # This initializer takes a backend-specific type, but it's
                # hidden from private subclasses.
                continue
            results.add(f"{c.__name__}.{f.__name__}{inspect.signature(f)}")
    return results
