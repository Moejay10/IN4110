#!/usr/bin/env python3

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy as np

ext_modules = [
            Extension(
                "instapy.gray.cython_color2gray",
                sources=["instapy/gray/cython_color2gray.pyx"],
                include_dirs=[np.get_include()]
            ),
            Extension(
                "instapy.sepia.cython_color2sepia",
                sources=["instapy/sepia/cython_color2sepia.pyx"],
                include_dirs=[np.get_include()]
            )
]

setup(
    ext_modules = ext_modules,
    cmdclass = {'build_ext': build_ext},
    name='Instapy',
    version='1.0',
    packages=['instapy'],
    package_data={'instapy': [
                                'grayscale_image.py', 'sepia_image.py',
                                'functions.py'
                                'gray/python_color2gray.py',
                                'gray/numpy_color2gray.py',
                                'gray/numba_color2gray.py',
                                'sepia/python_color2sepia.py',
                                'sepia/numpy_color2sepia.py',
                                'sepia/numba_color2sepia.py']},
    scripts=['bin/instapy'],
    install_requires=["tabulate", "datetime", "numpy", "pip>=19.3", "opencv-python", "numba", "cython"],
    test_requires=["pytest"],
)
