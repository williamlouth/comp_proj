from distutils.core import setup
from Cython.Build import cythonize

setup(name = 'Hello_world_app',ext_modules=cythonize("block.pyx"))

