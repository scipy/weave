#!/usr/bin/env python
from __future__ import absolute_import, print_function

from os.path import join


def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('weave',parent_package,top_path)
    config.add_data_dir('tests')
    config.add_data_dir('scxx')
    config.add_data_dir(join('blitz','blitz'))
    return config
