import numpy as np


def numpy_sepia(image, weights):
    """Converts an image to the sepia version of the original image

    Args:
        image (np.ndarray): A image represented in a ndarray. 3-dimensional ndarray.

    Returns:
        sepia_image (np.ndarray): A new ndarray representing the sepia version of the original image.

    """
    # Convert color values to sepia values
    output = np.dot(image, weights.T)
    # Combat overflow and setting the maximum value to 255 for each channel
    output[output > 255] = 255

    return output
