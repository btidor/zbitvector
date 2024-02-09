.. title:: zbitvector

.. include:: ../../README.md
    :end-before: ```py

.. literalinclude:: ../../README.md
    :start-after: ```py
    :end-before: ```

.. toctree::
    :maxdepth: 2

    api


Features
========

- Arrays::

    >>> A = Array[Uint8, Uint64](Uint64(0))
    >>> A[Uint8(1)] = Uint64(2)

- Simplification::

    >>> (Uint8(2) + Uint8(3)).reveal()
    5

- Solving::

    >>> s = Solver()
    >>> s.add(Uint8("X") + Uint8(1) == Uint8(0))
    >>> s.check()
    True

- Model Evaluation::

    >>> s.evaluate(Uint8("X"))
    255


Installation
============

Pre-built binary wheels are available on PyPI::

    pip install zbitvector

Wheels are built for the x86-64 and AArch64 architectures and support
these operating systems:

* macOS 10.9+
* Linux with glibc 2.17+ (*manylinux2014*)
* Linux with musl 1.1+ (*musllinux_1_1*)

zbitvector requires Python 3.8 or later.

To build from source, first `build Bitwuzla`_ using :code:`./configure --shared`
and install the library by running :code:`make install`.

.. _build Bitwuzla: https://github.com/bitwuzla/bitwuzla#readme

Runtime Options
===============

zbitvector uses the Bitwuzla solver by default, but can be configured to use Z3
by setting an environment variable::

    pip install z3-solver
    ZBITVECTOR_SOLVER=z3 python ...

zbitvector includes experimental optimizations which rewrite shift, extract and
if-then-else to be more compact and readable. These optimizations may cause
performance regressions. Try them out with::

    ZBITVECTOR_OPTIMIZE=1 python ...
