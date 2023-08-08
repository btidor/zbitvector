#!/usr/bin/env python3
"""A script to produce (rough) type stubs from reStructuredText markup."""

import enum
import inspect
import re

from zbitvector import pybitwuzla  # type: ignore

# pyright: reportUnnecessaryTypeIgnoreComment=false


def munge(expr: str) -> str:
    expr = re.sub(r"(list|tuple|dict)([^(])", r"\1[Any]\2", expr)
    expr = re.sub(r"(list|tuple|dict)\(([^)]+)\)", r"\1[\2]", expr)
    expr = expr.replace(" or ", " | ")
    expr = expr.replace("dict", "Dict")
    expr = expr.replace("list", "List")
    expr = expr.replace("tuple", "Tuple")
    expr = expr.replace("uint32_t", "int")
    expr = expr.replace("pybitwuzla.", "")
    expr = expr.replace("BitwuzlaOption", "Option")
    return expr


print("from __future__ import annotations")
print()
print("from enum import Enum")
print("from typing import Any, Dict, List, Tuple")
print()

for name, topic in inspect.getmembers(pybitwuzla):  # type: ignore
    if not inspect.isclass(topic):
        continue
    if inspect.getmodule(topic) != pybitwuzla:  # type: ignore
        continue

    if issubclass(topic, enum.Enum):
        assert topic.__doc__ is not None
        print(f"class {name}(Enum):")
        print(f'    """{topic.__doc__.strip()}"""')
        for item in topic.__members__.values():
            print(f"    {item.name} = {item.value}")
        print()
    else:
        parents = filter(
            lambda p: p != "object", map(lambda p: p.__name__, topic.__bases__)
        )
        print(f"class {name}({', '.join(parents)}):")
        printed = False
        for name, member in inspect.getmembers(topic):
            if "__objclass__" in dir(member) and member.__objclass__ != topic:
                continue
            if member.__doc__ is None:
                continue
            if name.startswith("__"):
                continue

            m = re.search(r":rtype:\s+(.+)\n", member.__doc__)
            if m is None:
                ret = "None"
            else:
                ret = munge(m.group(1))

            m = re.findall(r":type\s+([^:]+):\s+(.+)\n", member.__doc__)
            args = ["self"] + [f"{k}: {v}" for k, v in m]
            print(f"    def {name}({munge(', '.join(args))}) -> {ret}:")
            print(f'        """{member.__doc__.strip()}"""')
            print(f"        ...")
            print()
            printed = True

        if not printed:
            print(f"    ...")
