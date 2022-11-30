``scipy-weave`` provides tools for including C/C++ code within Python code.
Inlining C/C++ code within Python generally results in speedups of 1.5x to 30x
over algorithms written in pure Python.

``scipy-weave`` is the stand-alone version of the removed SciPy submodule
``scipy.weave``.   It is provided for users that need versions of SciPy from
which the ``weave`` submodule has been removed but have existing code that
still depends on ``scipy.weave``. **For new code, users are recommended to use
Cython.**

Note that the Python 3.x support is new as of version 0.19.0 (Nov 2022), and is
*experimental*. It is not tested on all Python 3.x versions.
For Python 2.6-2.7, use versions 0.17.0 or 0.18.0

To install ``scipy-weave``, use of pip is recommended:: 

    pip install scipy-weave

Note that the import name for ``scipy-weave`` is ``weave``. To run the tests::

     python -c "import weave; weave.test('full')"
