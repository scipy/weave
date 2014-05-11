Weave
=====

:Release: |release|
:Date: |today|

Weave provides tools for including C/C++ code within Python code. Inlining
C/C++ code within Python generally results in speedups of 1.5x to 30x over
algorithms written in pure Python.

Weave is the stand-alone version of the deprecated Scipy submodule
``scipy.weave``.   It is Python 2.x only, and is provided for users that need
new versions of Scipy (from which the ``weave`` submodule may be removed) but
have existing code that still depends on ``scipy.weave``.  For new code, users
are recommended to use Cython.


.. toctree::
   :maxdepth: 2

   release
   tutorial
   api_reference
