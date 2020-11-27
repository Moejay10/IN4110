class Array:
    # Assignment 3.3
    """
    Array is a class constructing arrays.

    The class consists of a constructor, methods for addition, subtraction,
    multiplication, equals, mean, variance, min_element and max_element.
    """

    def __init__(self, shape, *values):
        """
        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either numeric or boolean.

        Raises:
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """

        # Assigning values
        self._shape = shape
        self._values = values

        # Calculating the number of total values from the shape
        product = 1
        for element in self._shape:
            product *= element

        # Checking that the number of values fits with the shape given
        result = False
        if len(self._values) == product:
            # Checking that the values are all of the same type
            result = self.homogeneous_type(self._values)

        else:
            raise ValueError("The number of values does not fit with the shape given.")

        if result == False:
            raise ValueError("All the values given are not of the same datatype.")


        self._generate() # Creating the array

    def _generate(self):
        """Creates the array and assigns them the values.

        Returns:
        (if all the data type are of the same type)
            boolean: True or False

        """
        # Checks if shape is 2D
        if len(self._shape) == 1:
            self._array = [] # Creates empty 1D array
            for val in self._values:
                self._array.append(val)

        # Checks if shape is 2D
        elif len(self._shape) == 2:
            # Creates 2D array filled with zeros
            self._array = [[0 for column in range(self._shape[1])] for row in range(self._shape[0])]
            for i in range(self._shape[0]):
                for j in range(self._shape[1]):
                    self._array[i][j] = self._values[i*self._shape[1] + j]

        else:
            raise ValueError("The shape can only be 1D or 2D.")

    """
    def make_array(shape, values):
        data = 0
        while len(shape) > 0:
            data = [data for x in range(shape[-1])]
            shape.pop()
        return data
    """

    def homogeneous_type(self, seq):
        """Checks to see if given data types are of the same type.

        Args:
            seq (list): The list of values inputted into the class.

        Returns:
            bool: True if all the data type are of the same type. False otherwise.

        """
        iseq = iter(seq)
        first_type = type(next(iseq))
        if all( (type(x) is first_type) for x in iseq ):
            return True
        else:
            return False

    def numeric_type(self, seq):
        """Checks to see if given data types are numeric.

        Args:
            seq (list): The list of values inputted into the class.

        Returns:
            bool: True if all the data type are numeric. False otherwise.

        """
        iseq = iter(seq)
        if all( (isinstance(x, (float, int))) for x in iseq ):
            return True
        else:
            return False


    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """

        return "%s" % str(self._array)

    def __getitem__(self, index):
        """Returns single values of the array.
        Args:
            index (int): The index of the array.
        Returns:
            (int, float, str): The value of the array with the corresponding index.

        """
        return self._array[index]


    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """

        temp = Array(self._shape, *self._values)
        # Checking if array is 2D
        if len(self._shape) == 2:
            # Flattens the 2D array into 1D
            flattened1 = [val for sublist in temp for val in sublist]
            temp2 = (self._shape[0]*self._shape[1],)
            temp = Array(temp2, *flattened1) # Converting the 2D array into 1D

            # Checking if other is an array and 2D
            if isinstance(other, Array) and len(other._shape) == 2:
                # Flattens the 2D array into 1D
                flattened2 = [val for sublist in other for val in sublist]
                other_temp = (other._shape[0]*other._shape[1],)
                other = Array(other_temp, *flattened2) # Converting the 2D array into 1D

            # Checking if other is a numeric type
            elif isinstance(other, (int, float)):
                pass # Dont do anything

            else:
                return NotImplemented


        if not isinstance(other, Array): # Checking if other is not an array
            if isinstance(other, (int, float)):
                # If other is a number, adds it to the array elements
                for i in range(len(temp._array)):
                    temp._array[i] += other
            else:
                return NotImplemented
        else:
            for i in range(len(temp._array)): # Adds the two arrays together elementwise
                temp._array[i] += other._array[i]

        temp = Array(self._shape, *temp._array) # Creates the new array with new values

        return temp

    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        return self.__add__(other)


    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        temp = Array(self._shape, *self._values)
        # Checking if array is 2D
        if len(self._shape) == 2:
            # Flattens the 2D array into 1D
            flattened1 = [val for sublist in temp for val in sublist]
            temp2 = (self._shape[0]*self._shape[1],)
            temp = Array(temp2, *flattened1) # Converting the 2D array into 1D

            # Checking if other is an array and 2D
            if isinstance(other, Array) and len(other._shape) == 2:
                # Flattens the 2D array into 1D
                flattened2 = [val for sublist in other for val in sublist]
                other_temp = (other._shape[0]*other._shape[1],)
                other = Array(other_temp, *flattened2) # Converting the 2D array into 1D

            # Checking if other is a numeric type
            elif isinstance(other, (int, float)):
                pass # Dont do anything

            else:
                return NotImplemented


        if not isinstance(other, Array): # Checking if other is not an array
            if isinstance(other, (int, float)):
                # If other is a number, subtract it from the array elements
                for i in range(len(temp._array)):
                    temp._array[i] -= other
            else:
                return NotImplemented
        else:
            for i in range(len(temp._array)): # Subtracts the two arrays together elementwise
                temp._array[i] -= other._array[i]

        temp = Array(self._shape, *temp._array) # Creates the new array with new values

        return temp

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """
        if isinstance(other, (float, int)):
            temp_values = []
            for i in range(len(self._values)):
                temp_values.append(1*other)
            temp = Array(self._shape, *temp_values)
        return temp.__sub__(self)

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """

        temp = Array(self._shape, *self._values)
        # Checking if array is 2D
        if len(self._shape) == 2:
            # Flattens the 2D array into 1D
            flattened1 = [val for sublist in temp for val in sublist]
            temp2 = (self._shape[0]*self._shape[1],)
            temp = Array(temp2, *flattened1) # Converting the 2D array into 1D

            # Checking if other is an array and 2D
            if isinstance(other, Array) and len(other._shape) == 2:
                # Flattens the 2D array into 1D
                flattened2 = [val for sublist in other for val in sublist]
                other_temp = (other._shape[0]*other._shape[1],)
                other = Array(other_temp, *flattened2) # Converting the 2D array into 1D

            # Checking if other is a numeric type
            elif isinstance(other, (int, float)):
                pass # Dont do anything

            else:
                return NotImplemented


        if not isinstance(other, Array): # Checking if other is not an array
            if isinstance(other, (int, float)):
                # If other is a number, multiply it with the all array element
                for i in range(len(temp._array)):
                    temp._array[i] *= other
            else:
                return NotImplemented
        else:
            for i in range(len(temp._array)): # Multiply the two arrays together elementwise
                temp._array[i] *= other._array[i]

        temp = Array(self._shape, *temp._array) # Creates the new array with new values


        return temp

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal. False otherwise.

        """
        if isinstance(other, Array): # checking if other is an array

            # Checking if the shapes of the two arrays have the same shape
            if self._shape == other._shape and len(self._shape) == len(other._shape):

                # Checking if the two arrays have the same values
                if self._array == other._array:
                    return True

                else:
                    return False

            else:
                return False

        else:
            return False






    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        temp = Array(self._shape, *self._values)
        # Checking if array is 2D
        if len(self._shape) == 2:
            # Flattens the 2D array into 1D
            flattened1 = [val for sublist in temp for val in sublist]
            temp2 = (self._shape[0]*self._shape[1],)
            temp = Array(temp2, *flattened1) # Converting the 2D array into 1D

            # Checking if other is an array and 2D
            if isinstance(other, Array) and len(other._shape) == 2:
                # Flattens the 2D array into 1D
                flattened2 = [val for sublist in other for val in sublist]
                other_temp = (other._shape[0]*other._shape[1],)
                other = Array(other_temp, *flattened2) # Converting the 2D array into 1D

            # Checking if other is a numeric type
            elif isinstance(other, (int, float)):
                pass # Dont do anything

            else:
                return NotImplemented


        if not isinstance(other, Array): # Checking if other is not an array
            if isinstance(other, (int, float)):
                # If other is a number, checking if that number is equal to array element
                for i in range(len(temp._array)):
                    temp._array[i] =  temp._array[i] == other
            else:
                return NotImplemented
        else:
            for i in range(len(temp._array)): # Checking if the the two arrays have the same elements
                temp._array[i] = temp._array[i] == other._array[i]

        temp = Array(self._shape, *temp._array) # Creates the new array with new values


        return temp


    def mean(self):
        """Computes the mean of the array

        Only works for numeric data types.

        Returns:
            float: The mean of the array values.

        """
        temp = Array(self._shape, *self._values)
        # Checking if array is 2D
        if len(self._shape) == 2:
            # Flattens the 2D array into 1D
            flattened1 = [val for sublist in temp for val in sublist]
            temp2 = (self._shape[0]*self._shape[1],)
            temp = Array(temp2, *flattened1) # Converting the 2D array into 1D

        numeric = self.numeric_type(temp._array) # Checking if all the data types are numeric
        if numeric:
            mean = sum(temp._array)/len(temp._array) # Calculates the mean
            return mean

        else:
            print("Error: Only works for numeric data types.")
            return None

    def variance(self):
        """Computes the variance of the array

        Only works for numeric data types.
        The variance is computed as: mean((x - x.mean())**2)

        Returns:
            float: The mean of the array values.

        """
        temp = Array(self._shape, *self._values)
        # Checking if array is 2D
        if len(self._shape) == 2:
            # Flattens the 2D array into 1D
            flattened1 = [val for sublist in temp for val in sublist]
            temp2 = (self._shape[0]*self._shape[1],)
            temp = Array(temp2, *flattened1) # Converting the 2D array into 1D

        numeric = self.numeric_type(temp._array) # Checking if all the data types are numeric
        if numeric:
            mean = sum(temp._array)/len(temp._array) # Calculates mean
            variance = sum((x-mean)**2 for x in temp._array)/len(temp._array) # Calculates variance
            return variance

        else:
            print("Error: Only works for numeric data types.")
            return None

    def min_element(self):
        """Returns the smallest value of the array.

        Only works for numeric data types.

        Returns:
            float: The value of the smallest element in the array.

        """
        temp = Array(self._shape, *self._values)
        # Checking if array is 2D
        if len(self._shape) == 2:
            # Flattens the 2D array into 1D
            flattened1 = [val for sublist in temp for val in sublist]
            temp2 = (self._shape[0]*self._shape[1],)
            temp = Array(temp2, *flattened1) # Converting the 2D array into 1D

        numeric = self.numeric_type(temp._array) # Checking if all the data types are numeric
        if numeric:
            min = 1e10
            for element in temp._array:
                if min > element: # If the element is smaller than min, min is assigned a new value = element
                    min = element
            return min

        else:
            print("Error: Only works for numeric data types.")
            return None

    def max_element(self):
        """Returns the largest value of the array.

        Only works for numeric data types.

        Returns:
            float: The value of the largest element in the array.

        """
        temp = Array(self._shape, *self._values)
        # Checking if array is 2D
        if len(self._shape) == 2:
            # Flattens the 2D array into 1D
            flattened1 = [val for sublist in temp for val in sublist]
            temp2 = (self._shape[0]*self._shape[1],)
            temp = Array(temp2, *flattened1) # Converting the 2D array into 1D

        numeric = self.numeric_type(temp._array) # Checking if all the data types are numeric
        if numeric:
            max = -1e10
            for element in temp._array:
                if max < element: # If the element is bigger than max, max is assigned a new value = element
                    max = element
            return max

        else:
            print("Error: Only works for numeric data types.")
            return None
