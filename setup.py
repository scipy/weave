#!/usr/bin/env python
"""Weave: a C++ compiler for Python.

Weave provides tools for including C/C++ code within Python code. Inlining
C/C++ code within Python generally results in speedups of 1.5x to 30x over
algorithms written in pure Python.

Weave is the stand-alone version of the deprecated Scipy submodule
``scipy.weave``.   It is Python 2.x only, and is provided for users that need
new versions of Scipy (from which the ``weave`` submodule may be removed) but
have existing code that still depends on ``scipy.weave``.  For new code, users
are recommended to use Cython.

"""

DOCLINES = __doc__.split("\n")

import sys
import subprocess
import os

CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved
Programming Language :: C
Programming Language :: Python
Topic :: Software Development
Topic :: Scientific/Engineering
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS

"""


MAJOR               = 0
MINOR               = 18
MICRO               = 0
ISRELEASED          = False
VERSION             = '%d.%d.%d' % (MAJOR, MINOR, MICRO)


# Return the git revision as a string
def git_version():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout = subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = "Unknown"

    return GIT_REVISION


# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')


def get_version_info():
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    elif os.path.exists('weave/version.py'):
        # must be a source distribution, use existing version file
        # load it as a separate module to not load weave/__init__.py
        import imp
        version = imp.load_source('weave.version', 'weave/version.py')
        GIT_REVISION = version.git_revision
    else:
        GIT_REVISION = "Unknown"

    if not ISRELEASED:
        FULLVERSION += '.dev-' + GIT_REVISION[:7]

    return FULLVERSION, GIT_REVISION


def write_version_py(filename='weave/version.py'):
    cnt = """
# THIS FILE IS GENERATED FROM WEAVE SETUP.PY
short_version = '%(version)s'
version = '%(version)s'
full_version = '%(full_version)s'
git_revision = '%(git_revision)s'
release = %(isrelease)s

if not release:
    version = full_version
"""
    FULLVERSION, GIT_REVISION = get_version_info()

    with open(filename, 'w') as a:
        a.write(cnt % {'version': VERSION,
                       'full_version' : FULLVERSION,
                       'git_revision' : GIT_REVISION,
                       'isrelease': str(ISRELEASED)})


try:
    from sphinx.setup_command import BuildDoc
    HAVE_SPHINX = True
except:
    HAVE_SPHINX = False

if HAVE_SPHINX:
    class ScipyBuildDoc(BuildDoc):
        """Run in-place build before Sphinx doc build"""
        def run(self):
            ret = subprocess.call([sys.executable, sys.argv[0], 'build_ext', '-i'])
            if ret != 0:
                raise RuntimeError("Building Weave failed!")
            BuildDoc.run(self)


def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('weave')
    config.add_data_files(('weave', '*.txt'))

    config.get_version('weave/version.py')
    return config

def setup_package():

    # Rewrite the version file every time
    write_version_py()

    if HAVE_SPHINX:
        cmdclass = {'build_sphinx': ScipyBuildDoc}
    else:
        cmdclass = {}

    metadata = dict(
        name = 'weave',
        maintainer = "Weave developers",
        maintainer_email = "scipy-dev@scipy.org",
        description = DOCLINES[0],
        long_description = "\n".join(DOCLINES[2:]),
        url = "http://www.github.com/scipy/weave",
        download_url = "https://pypi.python.org/pypi/weave",
        license = 'BSD',
        cmdclass=cmdclass,
        classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
        platforms = ["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
        test_suite='nose.collector',
    )

    if len(sys.argv) >= 2 and ('--help' in sys.argv[1:] or
            sys.argv[1] in ('--help-commands', 'egg_info', '--version',
                            'clean')):
        # For these actions, NumPy is not required.
        #
        # They are required to succeed without Numpy for example when
        # pip is used to install Weave when Numpy is not yet present in
        # the system.
        try:
            from setuptools import setup
        except ImportError:
            from distutils.core import setup

        FULLVERSION, GIT_REVISION = get_version_info()
        metadata['version'] = FULLVERSION
    else:
        if len(sys.argv) >= 2 and sys.argv[1] in ['bdist_wheel', 'test']:
            # bdist_wheel needs setuptools
            import setuptools

        from numpy.distutils.core import setup
        metadata['configuration'] = configuration

    setup(**metadata)


if __name__ == '__main__':
    setup_package()
