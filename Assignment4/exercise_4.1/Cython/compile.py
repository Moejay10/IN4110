import numpy as np
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = [
            Extension(
                "cython_color2gray",
                sources=["*.pyx"],
                include_dirs=[np.get_include()]
            )
]

setup(
ext_modules = cythonize(ext_modules),
)
