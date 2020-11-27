import numpy as np
import time
import cv2
from tabulate import tabulate
import os
import datetime
import sys
from cython.view cimport array as cvarray

sys.path.append('../')
from functions import readImageFromFile, writeImageToFile, runTimes, gray_filter
from Python.python_color2gray import python_grayscale
from Numpy.numpy_color2gray import numpy_grayscale
from Numba.numba_color2gray import numba_grayscale


cpdef writeToReports(input_filename, image):
    """Writes a report containing the dimensions of the image
        being grayscaled that is, (H, W, C), along with the runtime of the function
        cython_grayscale.

    Args:
        input_filename (str): Filename of the image
        image (np.ndarray): A image represented in a ndarray. 3-dimensional ndarray.

    Returns:
        A report in a .txt format containing information of runtimes of the function
        python_grayscale.

    """

    # Initialize dimensions from input shape
    height, width, channel = image.shape

    # Create the table format for report
    table_time = []
    python_times, python_mean_time = runTimes(python_grayscale, image)
    numpy_times, numpy_mean_time = runTimes(numpy_grayscale, image)
    numba_times, numba_mean_time = runTimes(numba_grayscale, image, 4)
    cython_times, cython_mean_time = runTimes(cython_grayscale, image)

    compare_time1 = round(python_mean_time/cython_mean_time, 5)
    compare_time2 = round(numpy_mean_time/cython_mean_time, 5)
    compare_time3 = round(numba_mean_time/cython_mean_time, 5)


    a, b, c = cython_times
    column = 'cython_color2gray', a, b, c, cython_mean_time
    table_time.append(column)

    e = datetime.datetime.now()

    file_name = 'cython_report_color2gray.txt'

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

    file.write(f"Average runtime running cython_color2gray after 3 runs: {cython_mean_time} s \n")
    file.write(f"Average runtime running cython_color2gray is {compare_time1} times faster than python_color2gray \n")
    file.write(f"Average runtime running cython_color2gray is {compare_time2} times slower than numpy_color2gray \n")
    file.write(f"Average runtime running cython_color2gray is {compare_time3} times slower than numba_color2gray \n")
    file.write(f"Timing performed using: time module")

    file.write("\n")
    file.write("\n")
    file.write("#--------------------------------------------------------------------------#")
    file.write("\n")
    file.write("\n")

    file.close()

cpdef cython_grayscale(image):
    """Converts an image to the grayscale version of the original image

    Args:
        image (np.ndarray): A image represented in a ndarray. 3-dimensional ndarray.

    Returns:
        gray_image (np.ndarray): A new ndarray representing the gray version of the original image.

    """

    # Initialize dimensions from input shape
    cdef int height = image.shape[0]
    cdef int width = image.shape[1]
    cdef int channel = image.shape[2]
    cdef int h, w, c
    cdef double gray_pixel

    # Initialize weights and output
    weights = gray_filter()
    output = np.empty((height, width))
    output = output.astype('float64')

    # Cython memoryview of numpy array to make speedy Cython array operations
    cdef double[:, :, :] image_view = image.astype(np.dtype("d"))
    cdef double[:, :] output_view = output.astype(np.dtype('d'))
    cdef double[:] weights_view = weights.astype(np.dtype("d"))


    # Unvectorized
    for h in range(height): # Looping through height
        for w in range(width): # Looping through width
            gray_pixel = 0
            for c in range(channel): # Looping through channels
                gray_pixel += image_view[h,w,c]*weights_view[c]

            output_view[h,w] = gray_pixel

    # Vectorized
    #output_view = np.dot(image_view, weights_view.T)

    output[:, :] = output_view
    return output


cpdef main(input_filename, output_filename):
    """Reads an image from file,
        creates a gray version of the image, and writes
        the image to a file if output file is specified.

    Args:
        input_filename (str): Filename of the image

    """

    image = readImageFromFile(input_filename) # Reading in image from file

    gray_image = cython_grayscale(image) # Convert it to gray image

    writeImageToFile(gray_image, output_filename) # Write the gray image to file

    writeToReports(input_filename, image) # Write the reports
