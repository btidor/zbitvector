from __future__ import annotations

import inspect
from types import ModuleType

import zbitvector._abstract


def test_abstract():
    """Test that the current zbitvector backend matches the abstract spec."""
    assert _enumerate_module(zbitvector._abstract) == _enumerate_module(zbitvector)


def test_inheritance():
    assert issubclass(zbitvector.Constraint, zbitvector.Symbolic)
    assert not issubclass(zbitvector.Constraint, zbitvector.BitVector)
    assert issubclass(zbitvector.Uint, zbitvector.Symbolic)
    assert issubclass(zbitvector.Uint, zbitvector.BitVector)
    assert issubclass(zbitvector.Int, zbitvector.Symbolic)
    assert issubclass(zbitvector.Int, zbitvector.BitVector)
    assert not issubclass(zbitvector.Array, zbitvector.Symbolic)
    assert not issubclass(zbitvector.Array, zbitvector.BitVector)


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
