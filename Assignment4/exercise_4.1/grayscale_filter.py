import numpy as np
import argparse
import os
import cv2

from functions import readImageFromFile, writeImageToFile, gray_filter
from Python.python_color2gray import python_grayscale
from Numpy.numpy_color2gray import numpy_grayscale
from Numba.numba_color2gray import numba_grayscale
from Cython.cython_color2gray import cython_grayscale

def main():
    """Takes in an image an converts it into a gray image

    Returns:
        A gray image is returned

    """
    parser = argparse.ArgumentParser(
    description='Converts an image into a gray version of the original image.',
    formatter_class=argparse.RawTextHelpFormatter
    )


    parser.add_argument("-i", "--input", type=str, help="The input filename of file to apply filter to.", required=True)

    parser.add_argument("-sc", "--scale", type=float, help="Scale factor to resize image", default=1.0)

    parser.add_argument("-m", "--method",
                        help="Choose which implementation to use for filtering the image. ",
                        type=str, choices=['python', 'numpy', 'numba', 'cython'], default='numpy')

    parser.add_argument("-o", "--output", type=str, help="The output filename.", required=True)


    args = parser.parse_args()

    image = readImageFromFile(args.input)

    if args.scale != 1:
        image = cv2.resize(args.input, (0,0), fx=args.scale, fy=args.scale)

    if args.method == 'python':
        gray_image = python_grayscale(image)

    elif args.method == 'numpy':
        gray_image = numpy_grayscale(image)

    elif args.method == 'numba':
        gray_image = numba_grayscale(image)

    elif args.method == 'cython':
        gray_image = cython_grayscale(image)

    else:
        print("Wrong input given")



    writeImageToFile(gray_image, args.output)

if __name__ == '__main__':
    main()
