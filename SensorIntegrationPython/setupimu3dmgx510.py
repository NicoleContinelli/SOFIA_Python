#!/usr/bin/env python
"""
setup.py file for SWIG example
"""
from distutils.core import setup, Extension
from distutils import sysconfig
from Cython.Distutils import build_ext
import os

example_module = Extension('_imu3dmgx510',
sources=['imu3dmgx510_wrap.cxx', 'imu3dmgx510.cpp'],
extra_objects = ['_attitude_estimator.so', '_SerialComm.so'],
runtime_library_dirs = ['./'] ,swig_opts=['-Isrc','-c++']
)

class NoSuffixBuilder(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        suffix = sysconfig.get_config_var('EXT_SUFFIX')
        ext = os.path.splitext(filename)[1]
        return filename.replace(suffix, "") + ext
        
setup (name = 'imu3dmgx510',
version = '0.1',
author = "SWIG Docs",
description = """Simple swig example from docs""",
ext_modules = [example_module],
py_modules = ["imu3dmgx510"],
cmdclass={"build_ext": NoSuffixBuilder},
)

