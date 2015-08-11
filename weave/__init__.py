"""
C/C++ integration for Python

Main functions are::

  inline     -- a function for including C/C++ code within Python
  blitz      -- a function for compiling Numeric expressions to C++
  ext_tools  -- a module that helps construct C/C++ extension modules.
  accelerate -- a module that inline accelerates Python functions


.. note:: On Linux one needs to have the Python development headers installed
          in order to be able to compile things with the `weave` module.
          Since this is a runtime dependency these headers (typically in a
          pythonX.Y-dev package) are not always installed when installing
          weave.

"""
from __future__ import absolute_import, print_function

import sys


if not sys.version_info[:2] in [(2, 6), (2, 7)]:
    raise RuntimeError("Weave only supports Python 2.6 and 2.7")


from weave.version import version as __version__

from .blitz_tools import blitz, BlitzWarning
from .inline_tools import inline
from . import ext_tools
from .ext_tools import ext_module, ext_function
try:
    from .accelerate_tools import accelerate
except:
    pass


from numpy.testing import Tester
test = Tester().test
