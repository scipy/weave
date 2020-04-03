Weave provides tools for including C/C++ code within Python code. Inlining
C/C++ code within Python generally results in speedups of 1.5x to 30x over
algorithms written in pure Python.

Weave is the stand-alone version of the deprecated Scipy submodule
``scipy.weave``.   The official repo for weave supports Python 2.x only, and is provided for users that need
new versions of Scipy (from which the ``weave`` submodule may be removed) but
have existing code that still depends on ``scipy.weave``. This fork provides experimental support for Python 3.

To install Weave, use of pip is recommended:: 

    pip install weave

To run the tests::

    python2 -c "import weave; weave.test('full')"

