**zbitvector** is an efficient, well-typed interface to the Z3 and Bitwuzla SMT
solvers. It can be used to represent and manipulate symbolic expressions in the
theory of fixed-sized bitvectors and arrays (QF_BVA).

```py
import typing
import zbitvector

Uint8 = zbitvector.Uint[typing.Literal[8]]
Uint64 = zbitvector.Uint[typing.Literal[64]]

Uint64("X") + Uint64(1)
# => Uint64(`(bvadd X #x01)`)

Uint64("X") + Uint8(1)
# fails to typecheck
```

[Project homepage &rarr;](https://zbitvector.btidor.dev/)
