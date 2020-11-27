import numpy as np
import time
from tabulate import tabulate
import os
import sys

sys.path.append('../')
import test_slow_rectangle as tst


def Write_Results_To_File(file_name, function_names, table):
    """Writes a report that states the measured time of
        a specific function and compares it with other timing methods.

    Args:
        file (str): The file where the reports is written to
        comparison (list): A list containing the measured time for two other timing methods

    Returns:
        A report in a .txt format containing information of runtimes of a specific function

    """

    if os.path.isfile(file_name): # Checking if file exists
        os.remove(file_name) # Removes the file

    file = open(file_name, "a")

    # Prints the values in a nice tabulated form
    file.write(tabulate((table), headers=['Time module (s)',
    function_names[0], function_names[1], function_names[2], 'Slowest Part'], tablefmt='orgtbl'))

    file.close()


def manual_time(filename, compare = False):
    """Calculates the runtime of given functions using time module and
        writes the results to file

    Args:
        filename (str): Filename of the report
        Compares (bool): A variable to extract the runtime using timeit module

    """

    total_time = []

    function_names = ["random_array", "snake_loop", "loop"]



    # Timing the functions
    iterations = 3
    for i in range(iterations):

        start_time = time.time()
        array = tst.random_array(1e5)
        end_time = time.time()
        a = round(end_time - start_time, 5)

        start_time = time.time()
        filtered_array = tst.snake_loop(array)
        end_time = time.time()
        b = round(end_time - start_time, 5)

        start_time = time.time()
        filtered_array_snack = tst.loop(array)
        end_time = time.time()
        c = round(end_time - start_time, 5)

        # Creating the table format to the report
        if a > b and a > c:
            d = "random_array"
        elif b > a and b > c:
            d = "snake_loop"
        else:
            d = "loop"

        t = "Measurement " + str(i+1)
        column = t, a, b, c, d
        total_time.append(column)

    if compare:
        return total_time
    else:
        Write_Results_To_File(filename, function_names, total_time)

if __name__ == '__main__':
    manual_time("manual_report.txt")
