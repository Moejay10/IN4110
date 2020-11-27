import numpy as np


def python_grayscale(image, weights):
    """Converts an image to the grayscale version of the original image

    Args:
        image (np.ndarray): A image represented in a ndarray. 3-dimensional ndarray.

    Returns:
        gray_image (np.ndarray): A new ndarray representing the gray version of the original image.

    """

    # Initialize dimensions from input shape
    height, width, channel = image.shape

    # Initialize the output with zeros
    output = np.zeros([height, width])

    # Converting color pixels to gray pixels
    for h in range(height): # Looping through height
        for w in range(width): # Looping through width
            for c in range(channel): # Looping through channels
                output[h,w] += image[h,w,c]*weights[c]

    return output
