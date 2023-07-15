.. title:: zbitvector

.. include:: ../../README.md
    :end-before: ```py

.. literalinclude:: ../../README.md
    :start-after: ```py
    :end-before: ```

.. toctree::
    :maxdepth: 2

    api


Installation
============

zbitvector requires Python 3.8 or later. Pre-built binary wheels are available
for macOS and Linux on x86-64 and AArch64::

    pip install zbitvector

To build from source instead, first `build Bitwuzla`_ using :code:`./configure
--shared` and install the library by running :code:`make install`.

.. _build Bitwuzla: https://github.com/bitwuzla/bitwuzla#readme

zbitvector uses the Bitwuzla solver by default, but can be configured to use Z3
by setting an environment variable::

    pip install z3-solver
    ZBITVECTOR_SOLVER=z3 python ...
