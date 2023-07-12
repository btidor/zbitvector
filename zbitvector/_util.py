from __future__ import annotations

import abc
from typing import Any, Literal, cast, get_args, get_origin

from typing_extensions import Self


class BitVectorMeta(abc.ABCMeta):
    _ccache: dict[str, type] = {}

    def __getitem__(self, N: Any, /) -> Self:
        """
        Here's how Uint[N] (and Int[N]) work under the hood:

        At runtime, writing "Uint[N]" causes __getitem__(N) to be called on
        Uint's metaclass; "N" is an instance of typing.Literal. We unwrap the
        Literal to get the underlying int parameter n. Then we use `type()` to
        dynamically create a class, Uintn, which inherits from Uint and has the
        _sort attribute set based on n.

        Unfortunately, classes created with `type()` are invisible to the type
        checker. So, during type checking, "Uint[N]" is treated as an instance
        of the generic class Uint with type parameter N.
        """
        if isinstance(N, int):
            raise TypeError(
                f"integer passed to {self.__name__}[...]; use {self.__name__}[Literal[{N}]] instead"
            )

        if get_origin(N) != Literal:
            # No-op unbound type variables, unions, etc. These kind of Uint[...]
            # can be used in type signatures. Note that trying to instantiate
            # one will raise an error because _sort is not defined.
            return self

        args = get_args(N)
        if len(args) != 1 or not isinstance(args[0], int):
            raise TypeError(
                f"unsupported type parameter passed to {self.__name__}[...]"
            )

        n = args[0]
        if n <= 0:
            raise TypeError(f"{self.__name__} requires a positive width")

        name = self.__name__ + str(n)
        if name not in self._ccache:
            sort = cast(Any, self)._make_sort(n)
            cls = type(name, (self,), {"_sort": sort, "__slots__": ()})
            cls.__module__ = self.__module__
            self._ccache[name] = cls
        return cast(Self, self._ccache[name])
