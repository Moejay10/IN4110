import cv2

from instapy.functions import readImageFromFile, writeImageToFile, sepia_filter
from instapy.sepia.python_color2sepia import python_sepia
from instapy.sepia.numpy_color2sepia import numpy_sepia
from instapy.sepia.numba_color2sepia import numba_sepia
from instapy.sepia.cython_color2sepia import cython_sepia



def sepia(input_filename, method, scale_factor, k, output_filename=None):
    """Takes in an image an converts it into a sepia image

    Args:
        input_filename (str): Filename of the image
        method (str): Chooses which implementation to use
        scale_factor (float): Scales the image according to the factor
        k (float): Sepia effect factor
        output_filename (str): The filename of the gray image created

    Returns:
        If no output_filename is specified then
        the gray image is returned
        If output_filename is specified then
        the gray image written out

    """

    weights = sepia_filter(k) # Assigning the weights


    image = readImageFromFile(input_filename) # reading the file to image

    if scale_factor != 1: # If scaling is specified, the image is scaled accordingly
        image = cv2.resize(image, (0,0), fx=scale_factor, fy=scale_factor)

    if method == 'python':
        sepia_image = python_sepia(image, weights)

    elif method == 'numpy':
        sepia_image = numpy_sepia(image, weights)

    elif method == 'numba':
        sepia_image = numba_sepia(image, weights)

    elif method == 'cython':
        sepia_image = cython_sepia(image, weights)

    else:
        print("Wrong input given")

    # If no output filename is specified, the image array is returned
    if output_filename == None:
        return sepia_image

    # If output filename is specified, the image is written out
    else:
        writeImageToFile(sepia_image, output_filename)
