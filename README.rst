`weave` provides tools for including C/C++ code within Python code. Inlining
C/C++ code within Python generally results in speedups of 1.5x to 30x over
algorithms written in pure Python.

`weave` is the stand-alone version of the deprecated Scipy submodule
``scipy.weave``.   The official repo for `weave` supports Python 2.x only, and is provided for users that need
new versions of Scipy (from which the ``weave`` submodule may be removed) but
have existing code that still depends on ``scipy.weave``. This fork provides experimental support for Python 3.

For the moment, this experimental port of `weave`, is not on PyPI, so, if you would like to try it out, you can clone the repo and install it running pip from the root folder::

    pip install .

To run an example::

    python fibonacci.py
    
To run the tests::

    python runtests.py"

