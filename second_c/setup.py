from distutils.core import setup, Extension
import numpy as np


ext_modules = [Extension('test' ,sources=['test.c'])]

setup(
        name = "test",
        version = '1.0',
        include_dirs = [np.get_include()],
        ext_modules = ext_modules
        )
