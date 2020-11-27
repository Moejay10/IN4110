import cv2

from instapy.functions import readImageFromFile, writeImageToFile, gray_filter
from instapy.gray.python_color2gray import python_grayscale
from instapy.gray.numpy_color2gray import numpy_grayscale
from instapy.gray.numba_color2gray import numba_grayscale
from instapy.gray.cython_color2gray import cython_grayscale



def grayscale(input_filename, method, scale_factor, output_filename=None):
    """Takes in an image an converts it into a gray image

    Args:
        input_filename (str): Filename of the image
        method (str): Chooses which implementation to use
        scale_factor (float): Scales the image according to the factor
        output_filename (str): The filename of the gray image created

    Returns:
        If no output_filename is specified then
        the gray image is returned
        If output_filename is specified then
        the gray image written out

    """

    weights = gray_filter() # Assigning the weights

    image = readImageFromFile(input_filename) # reading the file to image

    if scale_factor != 1: # If scaling is specified, the image is scaled accordingly
        image = cv2.resize(image, (0,0), fx=scale_factor, fy=scale_factor)

    if method == 'python':
        gray_image = python_grayscale(image, weights)

    elif method == 'numpy':
        gray_image = numpy_grayscale(image, weights)

    elif method == 'numba':
        gray_image = numba_grayscale(image, weights)

    elif method == 'cython':
        gray_image = cython_grayscale(image, weights)

    else:
        print("Wrong input given")

    # If no output filename is specified, the image array is returned
    if output_filename == None:
        return gray_image

    # If output filename is specified, the image is written out
    else:
        writeImageToFile(gray_image, output_filename)
