import numpy as np
import cv2

from instapy.gray.python_color2gray import python_grayscale
from instapy.gray.numpy_color2gray import numpy_grayscale
from instapy.gray.numba_color2gray import numba_grayscale
from instapy.gray.cython_color2gray import cython_grayscale

from instapy.sepia.python_color2sepia import python_sepia
from instapy.sepia.numpy_color2sepia import numpy_sepia
from instapy.sepia.numba_color2sepia import numba_sepia
from instapy.sepia.cython_color2sepia import cython_sepia




def test_grayscale():
    """
    Testing that the grayscale_filter functions actually makes
    the images gray, by looking at the shape of the images.
    """

    # Arrange
    testArray = np.random.randint(255, size=(100, 150, 3))


    testArray = testArray.astype("uint8")

    # Initialize dimensions from weigths shape
    weights = np.array([0.21, 0.72, 0.07])

    test1 = python_grayscale(testArray, weights)
    assert len(test1.shape) == 2

    test2 = numpy_grayscale(testArray, weights)
    assert len(test2.shape) == 2

    test3 = numba_grayscale(testArray, weights)
    assert len(test3.shape) == 2

    test4 = cython_grayscale(testArray, weights)
    assert len(test4.shape) == 2


def test_sepia():
    """
    Testing that the sepia_filter functions actually changes
    the images with a sepia filter, by checking a
    sepia image created from the different implementation
    against the expected weighted values.
    """
    # Arrange
    testArray = np.random.randint(255, size=(100, 150, 3))
    testArray.astype('float64')
    # Initialize dimensions from weigths shape
    weights = np.array([[0.393, 0.769, 0.189],
                        [0.349, 0.686, 0.168],
                        [0.272, 0.534, 0.131]])


    weights = np.flip(weights)

    testArray2 = testArray.dot(weights.T)
    testArray2[testArray2 > 255] = 255

    test1 = python_sepia(testArray, weights)
    assert np.array_equal(test1, testArray2)

    test2 = numpy_sepia(testArray, weights)
    assert np.array_equal(test2, testArray2)

    test3 = numba_sepia(testArray, weights)
    assert np.array_equal(test3, testArray2)

    test4 = cython_sepia(testArray, weights)
    assert np.array_equal(test4, testArray2)
