from distutils.core import setup,Extension

module1 = Extension('spam',
        sources =['spammodule.c'])

setup (name = 'spam',
        version = 1.0,
        description = 'test',
        ext_modules = [module1])
