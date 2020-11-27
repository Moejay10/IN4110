from unittest import TestCase

from array import Array

import numpy as np # Using numpy to test the Array class

class TestArray(TestCase):
    pass

    # Test cases for 1D arrays

    def test_1D_printstatement(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        answer = [2, 3, 1, 0]
        assert vec1.__str__() == str(answer)

    def test_1D_getitem(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        answer = [2, 3, 1, 0]
        assert vec1[2] == answer[2]

    def test_1D_addition_with_number(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = vec1 + 1
        answer = Array((4,), 3, 4, 2, 1)
        assert a == answer

    def test_1D_addition_with_number_reversed(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = 1 + vec1
        answer = Array((4,), 3, 4, 2, 1)
        assert a == answer

    def test_1D_addition_with_array(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = vec1 + vec1
        answer = Array((4,), 4, 6, 2, 0)
        assert a == answer

    def test_1D_subtraction_with_number(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = vec1 - 1
        answer = Array((4,) ,1, 2, 0, -1)
        assert a == answer

    def test_1D_subtraction_with_number_reversed(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = 1 - vec1
        answer = Array((4,) ,-1, -2, 0, 1)
        assert a == answer

    def test_1D_subtraction_with_array(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = vec1 - vec1
        answer = Array((4,) ,0, 0, 0, 0)
        assert a == answer

    def test_1D_multiplication_with_number(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = vec1 * 2
        answer = Array((4,) ,4, 6, 2, 0)
        assert a == answer

    def test_1D_multiplication_with_number_reversed(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = 2 * vec1
        answer = Array((4,) ,4, 6, 2, 0)
        assert a == answer

    def test_1D_multiplication_with_array(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = vec1 * vec1
        answer = Array((4,) ,4, 9, 1, 0)
        assert a == answer

    def test_1D_equal(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        vec2 = Array((4,), 2, 3, 1, 0)
        assert vec1 == vec2

    def test_1D_not_equal(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        vec2 = Array((4,), 8, 3, 4, 1)
        assert vec1 != vec2

    def test_1D_is_equal_with_array(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        vec2 = Array((4,), 2, 3, -1, 0)
        answer = Array((4,) ,True, True, False, True)
        assert vec1.is_equal(vec2) == answer

    def test_1D_is_not_equal_with_array(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        vec2 = Array((4,), 2, 3, 0, 0)
        answer = Array((4,) ,False, True, False, True)
        assert vec1.is_equal(vec2) != answer

    def test_1D_is_equal_with_number(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        n = 8
        answer = Array((4,) ,False, False, False, False)
        assert vec1.is_equal(n) == answer

    def test_1D_is_not_equal_with_number(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        n = 8
        answer = Array((4,) ,False, True, True, False)
        assert vec1.is_equal(n) != answer

    def test_1D_is_mean(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = np.array([2, 3, 1, 0])
        assert vec1.mean() == np.mean(a)

    def test_1D_is_not_mean(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = np.array([4, -3, 1, 5])
        assert vec1.mean() != np.mean(a)

    def test_1D_is_variance(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = np.array([2, 3, 1, 0])
        assert vec1.variance() == np.var(a)

    def test_1D_is_not_variance(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = np.array([4, -3, 1, 5])
        assert vec1.variance() != np.var(a)

    def test_1D_is_min_element(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = np.array([2, 3, 1, 0])
        assert vec1.min_element() == np.min(a)

    def test_1D_is_not_min_element(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = np.array([4, -3, 1, 5])
        assert vec1.min_element() != np.min(a)

    def test_1D_is_max_element(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = np.array([2, 3, 1, 0])
        assert vec1.max_element() == np.max(a)

    def test_1D_is_not_max_element(self):
        vec1 = Array((4,), 2, 3, 1, 0)
        a = np.array([4, -3, 1, 5])
        assert vec1.max_element() != np.max(a)


    # Test cases for 2D arrays

    def test_2D_printstatement(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        answer = [[8, 3], [4, 1], [6, 1]]
        assert my_array.__str__() == str(answer)

    def test_2D_getitem(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        answer = [[8, 3], [4, 1], [6, 1]]
        assert my_array[1][0] == answer[1][0]

    def test_2D_addition_with_number(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = my_array + 1
        answer = Array((3,2), 9, 4, 5, 2, 7, 2)
        assert a == answer

    def test_2D_addition_with_number_reversed(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = 1 + my_array
        answer = Array((3,2), 9, 4, 5, 2, 7, 2)
        assert a == answer

    def test_2D_addition_with_array(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = my_array + my_array
        answer = Array((3,2), 16, 6, 8, 2, 12, 2)
        assert a == answer

    def test_2D_subtraction_with_number(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = my_array - 1
        answer = Array((3,2), 7, 2, 3, 0, 5, 0)
        assert a == answer

    def test_2D_subtraction_with_number_reversed(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = 1 - my_array
        answer = Array((3,2), -7, -2, -3, 0, -5, 0)
        assert a == answer

    def test_2D_subtraction_with_array(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = my_array - my_array
        answer = Array((3,2), 0, 0, 0, 0, 0, 0)
        assert a == answer

    def test_2D_multiplication_with_number(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = my_array * 2
        answer = Array((3,2), 16, 6, 8, 2, 12, 2)
        assert a == answer

    def test_2D_multiplication_with_number_reversed(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = 2 * my_array
        answer = Array((3,2), 16, 6, 8, 2, 12, 2)
        assert a == answer

    def test_2D_multiplication_with_array(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = my_array * my_array
        answer = Array((3,2), 64, 9, 16, 1, 36, 1)
        assert a == answer

    def test_2D_equal(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        my_array2 = Array((3,2), 8, 3, 4, 1, 6, 1)
        assert my_array == my_array2

    def test_2D_not_equal(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        my_array2 = Array((3,2), 8, 0, 4, 5, 6, 10)
        assert my_array != my_array2

    def test_2D_is_equal_with_array(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        my_array2 = Array((3,2), 8, 0, 4, 5, 6, 10)
        answer = Array((3,2), True, False, True, False, True, False)
        assert my_array.is_equal(my_array2) == answer

    def test_2D_is_not_equal_with_array(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        my_array2 = Array((3,2), 8, 0, 4, 5, 6, 10)
        answer = Array((3,2), True, True, True, True, True, False)
        assert my_array.is_equal(my_array2) != answer

    def test_2D_is_equal_with_number(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        n = 8
        answer = Array((3,2), True, False, False, False, False, False)
        assert my_array.is_equal(n) == answer

    def test_2D_is_not_equal_with_number(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        n = 8
        answer = Array((3,2), True, False, True, True, False, False)
        assert my_array.is_equal(n) != answer

    def test_2D_is_mean(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = np.array([[8, 3], [4, 1], [6, 1]])
        assert my_array.mean() == np.mean(a)

    def test_2D_is_not_mean(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = np.array([[0, 3], [5, 1], [16, 1]])
        assert my_array.mean() != np.mean(a)

    def test_2D_is_variance(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = np.array([[8, 3], [4, 1], [6, 1]])
        assert my_array.variance() == np.var(a)

    def test_2D_is_not_variance(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = np.array([[0, 3], [5, 1], [16, 1]])
        assert my_array.variance() != np.var(a)

    def test_2D_is_min_element(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = np.array([[8, 3], [4, 1], [6, 1]])
        assert my_array.min_element() == np.min(a)

    def test_2D_is_not_min_element(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = np.array([[0, 3], [5, 1], [16, 1]])
        assert my_array.min_element() != np.min(a)

    def test_2D_is_max_element(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = np.array([[8, 3], [4, 1], [6, 1]])
        assert my_array.max_element() == np.max(a)

    def test_2D_is_not_max_element(self):
        my_array = Array((3,2), 8, 3, 4, 1, 6, 1)
        a = np.array([[0, 3], [5, 1], [16, 1]])
        assert my_array.max_element() != np.max(a)
