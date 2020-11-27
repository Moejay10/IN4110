import numpy as np
from cython.view cimport array as cvarray

cpdef cython_grayscale(image, weights):
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
