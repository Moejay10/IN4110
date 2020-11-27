import numpy as np


def numpy_grayscale(image, weights):
    """Converts an image to the grayscale version of the original image

    Args:
        image (np.ndarray): A image represented in a ndarray. 3-dimensional ndarray.

    Returns:
        gray_image (np.ndarray): A new ndarray representing the gray version of the original image.

    """
    # Converting color pixels to gray pixels
    output = image.dot(weights.T)
    return output
