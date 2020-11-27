import numpy as np
import argparse
import os
import cv2

from functions import readImageFromFile, writeImageToFile, sepia_filter
from Python.python_color2sepia import python_sepia
from Numpy.numpy_color2sepia import numpy_sepia
from Numba.numba_color2sepia import numba_sepia
from Cython.cython_color2sepia import cython_sepia

def main():
    """Takes in an image an converts it into a sepia image

    Returns:
        A sepia image is returned

    """
    parser = argparse.ArgumentParser(
    description='Converts an image into a sepia version of the original image.',
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
        sepia_image = python_sepia(image)

    elif args.method == 'numpy':
        sepia_image = numpy_sepia(image)

    elif args.method == 'numba':
        sepia_image = numba_sepia(image)

    elif args.method == 'cython':
        sepia_image = cython_sepia(image)

    else:
        print("Wrong input given")



    writeImageToFile(sepia_image, args.output)

if __name__ == '__main__':
    main()
