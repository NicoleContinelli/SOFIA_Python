#!/usr/bin/env python
"""
setup.py file for SWIG example
"""
from distutils.core import setup, Extension
from distutils import sysconfig
from Cython.Distutils import build_ext
import os

example_module = Extension('_Cia402device',
sources=['Cia402device_wrap.cxx', 'Cia402device.cpp'],
extra_objects = ['_PortBase.so', '_SocketCanPort.so', '_CiA301CommPort.so', '_CiA402SetupData.so' ],
runtime_library_dirs = ['./'] ,swig_opts=['-Isrc','-c++']
)

class NoSuffixBuilder(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        suffix = sysconfig.get_config_var('EXT_SUFFIX')
        ext = os.path.splitext(filename)[1]
        return filename.replace(suffix, "") + ext
        
setup (name = 'Cia402device',
version = '0.1',
author ="Nicole & Luis",
description = """Simple swig example from docs""",
ext_modules = [example_module],
py_modules = ["Cia402device"],
cmdclass={"build_ext": NoSuffixBuilder},
)
