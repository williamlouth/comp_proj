import numpy
from distutils.core import setup,Extension
setup(name="custom",version=1.0,
        ext_modules=[Extension("custom",['custom.c'],include_dirs=[numpy.get_include()])])
