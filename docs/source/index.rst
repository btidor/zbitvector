.. title:: zbitvector

**zbitvector** is an efficient, well-typed interface to the Z3 and Bitwuzla SMT
solvers. It can be used to represent and manipulate symbolic expressions in the
theory of fixed-sized bitvectors and arrays (QF_BVA).

::

    from zbitvector import BitVector

    Uint8  = BitVector.subclass(8)
    Uint64 = BitVector.subclass(64)

    Uint64("A") + Uint64(1)
    # => Uint64(`(bvadd A #x01)`)

    Uint64("A") + Uint8(1)
    # fails to typecheck

Installation
============

zbitvector requires Python 3.8 or later. Pre-built binary wheels are available
for macOS and Linux on x86-64 and AArch64::

    pip install zbitvector

To build from source instead, first `build Bitwuzla`_ using :code:`./configure
--shared` and install the library by running :code:`make install`.

.. _build Bitwuzla: https://github.com/bitwuzla/bitwuzla#readme

.. toctree::
   :maxdepth: 2
   :caption: Contents:
