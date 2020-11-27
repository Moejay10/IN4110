import numpy as np
import time
import cv2
from tabulate import tabulate
import os
import sys
import datetime

sys.path.append('../')
from functions import readImageFromFile, writeImageToFile, runTimes, sepia_filter
from Python.python_color2sepia import python_sepia
from Numpy.numpy_color2sepia import numpy_sepia
from Numba.numba_color2sepia import numba_sepia


cpdef writeToReports(input_filename, image):
    """Writes a report containing the dimensions of the image
        being sepiad that is, (H, W, C), along with the runtime of the function
        python_sepia.

    Args:
        input_filename (str): Filename of the image
        image (numpy.ndarray): A image represented in a ndarray. 3-dimensional ndarray.

    Returns:
        A report in a .txt format containing information of runtimes of the function
        python_sepia.

    """

    # Initialize dimensions from input shape
    height, width, channel = image.shape

    table_time = []
    python_times, python_mean_time = runTimes(python_sepia, image)
    numpy_times, numpy_mean_time = runTimes(numpy_sepia, image)
    numba_times, numba_mean_time = runTimes(numba_sepia, image, 4)
    cython_times, cython_mean_time = runTimes(cython_sepia, image)

    compare_time1 = round(python_mean_time/cython_mean_time, 5)
    compare_time2 = round(numpy_mean_time/cython_mean_time, 5)
    compare_time3 = round(numba_mean_time/cython_mean_time, 5)


    a, b, c = cython_times
    column = 'cython_color2sepia', a, b, c, cython_mean_time
    table_time.append(column)

    e = datetime.datetime.now()

    file_name = 'cython_report_color2sepia.txt'

    if os.path.isfile(file_name): # Checking if file exists
        os.remove(file_name) # Removes the file


    file = open(file_name, "a")

    file.write(f"Last run date was %s/%s/%s at %s:%s:%s \n" % (e.day, e.month, e.year, e.hour, e.minute, e.second ))
    file.write("\n")
    file.write("\n")
    file.write("#--------------------------------------------------------------------------#")
    file.write("\n")
    file.write("\n")

    file.write(f"The picture used is the default size of {input_filename} which has size of {height, width, channel} \n")
    file.write("\n")
    file.write("\n")

    # Prints the values in a nice tabulated form
    file.write(tabulate((table_time), headers=['Time (s)', 'Run 1', 'Run 2', 'Run 3', 'Mean'], tablefmt='orgtbl'))

    file.write("\n")
    file.write("\n")
    file.write("#--------------------------------------------------------------------------#")
    file.write("\n")
    file.write("\n")

    file.write(f"Average runtime running cython_color2sepia after 3 runs: {cython_mean_time} s \n")
    file.write(f"Average runtime running cython_color2sepia is {compare_time1} times faster than python_color2sepia \n")
    file.write(f"Average runtime running cython_color2sepia is {compare_time2} times slower than numpy_color2sepia \n")
    file.write(f"Average runtime running cython_color2sepia is {compare_time3} times slower than numba_color2sepia \n")
    file.write(f"Timing performed using: time module")

    file.write("\n")
    file.write("\n")
    file.write("#--------------------------------------------------------------------------#")
    file.write("\n")
    file.write("\n")

    file.close()

cpdef cython_sepia(image):
    """Converts an image to the sepia version of the original image

    Args:
        image (numpy.ndarray): A image represented in a ndarray. 3-dimensional ndarray.

    Returns:
        sepia_image (numpy.ndarray): A new ndarray representing the sepia version of the original image.

    """
    # Initialize dimensions from weigths shape
    weights = sepia_filter()

    # Convert color values to sepia values
    output = np.dot(image, weights.T)
    # Combat overflow and setting the maximum value to 255 for each channel
    output[output > 255] = 255


    return output


cpdef main(input_filename, output_filename):
    """Reads an image from file,
    creates a sepia version of the image, and writes
    the image to a file if output file is specified.

    Args:
      input_filename (str): Filename of the image

    """
    image = readImageFromFile(input_filename) # Reading in image from file

    sepia_image = cython_sepia(image) # Using sepia filter image

    writeImageToFile(sepia_image, output_filename) # Write the new image to file

    writeToReports(input_filename, image) # Write the reports
