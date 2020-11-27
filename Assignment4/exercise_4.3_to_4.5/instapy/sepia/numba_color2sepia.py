import numpy as np
from numba import jit


@jit(nopython=True)
def numba_sepia(image, weights):
    """Converts an image to the sepia version of the original image

    Args:
        image (np.ndarray): A image represented in a ndarray. 3-dimensional ndarray.

    Returns:
        sepia_image (np.ndarray): A new ndarray representing the sepia version of the original image.

    """
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
