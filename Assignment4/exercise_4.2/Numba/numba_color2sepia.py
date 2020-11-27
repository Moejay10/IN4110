import numpy as np
import timeit
import cv2
from tabulate import tabulate
import os
import sys
import datetime
from numba import jit

sys.path.append('../')
from functions import readImageFromFile, writeImageToFile, runTimes, sepia_filter
from Python.python_color2sepia import python_sepia
from Numpy.numpy_color2sepia import numpy_sepia


def writeToReports(input_filename, image):
    """Writes a report containing the dimensions of the image
        being sepiad that is, (H, W, C), along with the runtime of the function
        python_sepia.

    Args:
        input_filename (str): Filename of the image
        image (np.ndarray): A image represented in a ndarray. 3-dimensional ndarray.

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

    compare_time1 = round(python_mean_time/numba_mean_time, 5)
    compare_time2 = round(numpy_mean_time/numba_mean_time, 5)

    a, b, c = numba_times
    column = 'numba_color2sepia', a, b, c, numba_mean_time
    table_time.append(column)

    e = datetime.datetime.now()

    file_name = 'numba_report_color2sepia.txt'

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

    file.write(f"Average runtime running numba_color2sepia after 3 runs: {numba_mean_time} s \n")
    file.write(f"Average runtime running numba_color2sepia is {compare_time1} times faster than python_color2sepia \n")
    file.write(f"Average runtime running numba_color2sepia is {compare_time2} times faster than numpy_color2sepia \n")
    file.write(f"Timing performed using: time module")

    file.write("\n")
    file.write("\n")
    file.write("#--------------------------------------------------------------------------#")
    file.write("\n")
    file.write("\n")


    file.write(f"The advantage with numba is that it is easy to implement \nand usually very little code change is required for the program to run. \n")
    file.write("\n")
    file.write(f"The disadvantage with numba is that it works like a 'black box', \nwhich can make it difficult to understand which in turn makes it harder to debug.")

    file.close()

@jit(nopython=True)
def numba_sepia(image):
    """Converts an image to the sepia version of the original image

    Args:
        image (np.ndarray): A image represented in a ndarray. 3-dimensional ndarray.

    Returns:
        sepia_image (np.ndarray): A new ndarray representing the sepia version of the original image.

    """

    # Initialize dimensions from weigths shape
    weights = np.array([[0.393, 0.769, 0.189],
                        [0.349, 0.686, 0.168],
                        [0.272, 0.534, 0.131]])

    weights = np.flip(weights)

    # Initialize dimensions from input shape
    height, width, channel = image.shape

    # Prepare array for storing sepia image
    output = np.zeros_like(image, dtype=np.float64)

    # Convert color values to sepia values
    for h in range(height):
        for w in range(width):
            for c in range(channel):
                for i in range(len(weights[0])):
                    output[h, w, c] += image[h, w, i]*weights[c][i]

                # Combat overflow and setting the maximum value to 255 for each channel
                if output[h, w, c] > 255:
                    output[h, w, c] = 255

    return output



def main(input_filename, output_filename):
    """Reads an image from file,
    creates a sepia version of the image, and writes
    the image to a file if output file is specified.

    Args:
        input_filename (str): Filename of the image

    """


    image = readImageFromFile(input_filename) # Reading in image from file

    sepia_image = numba_sepia(image) # Using sepia filter image

    writeImageToFile(sepia_image, output_filename) # Write the new image to file

    writeToReports(input_filename, image) # Write the reports



if __name__ == '__main__':

    main('../rain.jpg', 'numba_rain_sepia.jpg')
