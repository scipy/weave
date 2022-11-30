``scipy-weave`` provides tools for including C/C++ code within Python code.
Inlining C/C++ code within Python generally results in speedups of 1.5x to 30x
over algorithms written in pure Python.

``scipy-weave`` is the stand-alone version of the removed SciPy submodule
``scipy.weave``.   It is Python 2.x only, and is provided for users that need
versions of SciPy from which the ``weave`` submodule has been removed but
have existing code that still depends on ``scipy.weave``.  For new code, users
are recommended to use Cython.

To install ``scipy-weave``, use of pip is recommended:: 

    pip install scipy-weave

Note that the import name for ``scipy-weave`` is ``weave``. To run the tests::

    python2 -c "import weave; weave.test('full')"

