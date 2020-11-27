import numpy as np
import time
import cv2
import os

def readImageFromFile(filename='rain.jpg'):
    """Reads in an image from a file

    Args:
        filename (str): Filename of the image

    Returns:
        image (np.ndarray): Numpy ndarray of 3 dimensions from the cv2.imread function

    Raises:
        FileNotFoundError: if file is not found

    """

    if os.path.isfile(filename) == False:
        raise FileNotFoundError("Could not open or read file given")
    else:

        if type(filename) is not np.ndarray:
            # Image stored as a file can be loaded to a Numpy array as done below
            image = cv2.imread(filename) # OpenCV uses BGR, but it is common to use RGB
        else:
            image = filename

        image = image.astype('float64') # Converts elements from uint8 to float
        return image

def writeImageToFile(image, output_filename):
    """Writing an image to file

    Args:
        image (np.ndarray): An image represented in a ndarray with 3-dimensions ndarray.
        filename (str): Filename of the outfile

    Returns:
        image (np.ndarray): Numpy ndarray of 3 dimensions from the cv2.imread function

    Raises:
        FileNotFoundError: if file is not found

    """
    new_image = image.astype("uint8")
    cv2.imwrite(output_filename, new_image)


def runTimes(func, image, num_runs=3):
    """Calculates the runtime of given function

    Args:
        func (function): A function that converts an image to the gray version of it
        image (np.ndarray): A image represented in a ndarray. 3-dimensional ndarray.

    Returns:
        times (list): A list containing all the runtimes of the given function
        mean_time (float): The mean time of all the runtimes of the given function
    """

    times = []
    for i in range(num_runs):
        start_time = time.time()
        grayscale_image = func(image)
        end_time = time.time()
        a = round(end_time - start_time, 5)
        times.append(a)

    if num_runs > 3:
        times.pop(0) # NUMBA: DO NOT REPORT THIS... COMPILATION TIME IS INCLUDED IN THE EXECUTION TIME!

    mean_time = round(sum(times)/len(times), 5)

    return times, mean_time

def sepia_filter(k):
    """Creates the filter for sepia

    Args:
        k (float): Sepia effect factor

    Returns:
        weights (np.array): A filter to turn images vintage
    """
    # Initialize dimensions from weigths shape
    weights = np.array([[ 0.393 + 0.607 * (1 - k), 0.769 - 0.769 * (1 - k), 0.189 - 0.189 * (1 - k)],
                        [ 0.349 - 0.349 * (1 - k), 0.686 + 0.314 * (1 - k), 0.168 - 0.168 * (1 - k)],
                        [ 0.272 - 0.272 * (1 - k), 0.534 - 0.534* (1 - k), 0.131 + 0.869 * (1 - k)]])

    weights = np.flip(weights) # Turning into BGR from RGB format

    return weights

def gray_filter():
    """Creates the filter for gray

    Returns:
        weights (np.array): A filter to turn images gray
    """
    # Initialize dimensions from weigths shape
    weights = np.array([0.21, 0.72, 0.07]) # RGB format
    weights = np.flip(weights) # Turning into BGR format

    return weights
