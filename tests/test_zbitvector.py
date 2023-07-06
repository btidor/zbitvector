#!/usr/bin/env pytest

from __future__ import annotations

import inspect
import typing
from types import ModuleType

import pytest

from zbitvector import Int, _backend, _bitwuzla  # pyright: ignore[reportPrivateUsage]


def test_init_validations():
    with pytest.raises(TypeError, match=f"Cannot instantiate Int directly"):
        Int(123)

    with pytest.raises(TypeError, match="Unknown type parameter passed to Int"):
        Int[typing.Literal["asdf"]]  # type: ignore

    with pytest.raises(TypeError, match="Int requires a positive width"):
        Int[typing.Literal[-1]]


def test_backend_api():
    assert enumerate_module(_backend) == enumerate_module(_bitwuzla)


def enumerate_module(module: ModuleType) -> set[str]:
    results: set[str] = set()
    for _, c in inspect.getmembers(module):
        if not inspect.isclass(c):
            continue
        if inspect.getmodule(c) != inspect.getmodule(module):
            continue
        for _, f in inspect.getmembers(c):
            if not inspect.isfunction(f):
                continue
            if f.__name__.startswith("_") and not f.__name__.startswith("__"):
                continue
            if c.__name__ == "Symbolic" and f.__name__ == "__init__":
                # This initializer takes a backend-specific type, but it's
                # hidden from private subclasses.
                continue
            results.add(f"{c.__name__}.{f.__name__}{inspect.signature(f)}")
    return results
