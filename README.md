**zbitvector** is an efficient, well-typed interface to the Z3 and Bitwuzla SMT
solvers. It can be used to represent and manipulate symbolic expressions in the
theory of fixed-sized bitvectors and arrays (QF_BVA).

```py
import zbitvector

class Uint8(zbitvector.Uint):
    width = 8

class Uint64(zbitvector.Uint):
    width = 64

Uint64("A") + Uint64(1)
# => Uint64(`(bvadd A #x01)`)

Uint64("A") + Uint8(1)
# fails to typecheck
```

[Project homepage &rarr;](https://zbitvector.btidor.dev/)
