import numpy as np
import timeit
from tabulate import tabulate
import os
import sys

sys.path.append('../')
import test_slow_rectangle as tst
from manual_Time.manual_timing_ import manual_time


def Write_Results_To_File(file_name, function_names, table1, table2, comparison):
    """Writes a report that states the measured time of
        a specific function and compares it with other timing methods.

    Args:
        file_name (str): The file where the reports is written to
        function_names (list): List containing the function names
        table1 (list): List containing the runtimes of timeit
        table2 (list): List containing the runtimes of manual time
        comparison (list): A list containing the measured time for two other timing methods

    Returns:
        A report in a .txt format containing information of runtimes of a specific function

    """

    if os.path.isfile(file_name): # Checking if file exists
        os.remove(file_name) # Removes the file

    file = open(file_name, "a")

    # Prints the values in a nice tabulated form
    file.write(tabulate((table1), headers=['Timeit module (s)', function_names[0],
    function_names[1], function_names[2], 'Slowest Part'], tablefmt='orgtbl'))

    file.write("\n")
    file.write("\n")
    file.write("#--------------------------------------------------------------------------#")
    file.write("\n")
    file.write("\n")

    # Prints the values in a nice tabulated form
    file.write(tabulate((table2), headers=['Manual Time (s)', function_names[0],
    function_names[1], function_names[2], 'Slowest Part'], tablefmt='orgtbl'))

    file.write("\n")
    file.write("\n")
    file.write("#--------------------------------------------------------------------------#")
    file.write("\n")
    file.write("\n")

    file.write(f"The slowest time found by timeit module was {comparison[0]}s \n")
    file.write(f"Compared to {comparison[1]}s found by manual timing")

    file.close()


def compare(list):
    """Finds the slowest runtime of three functions.

    Args:
        list (list): A list containing the measured time for three functions.

    Returns:
        slowest_time (float): The slowest measured runtime of three functions.

    """
    # Creating empty lists to store results
    array_times = []
    snake_loop_times = []
    loop_times = []
    slowest_part = []
    for i in range(len(list)):
        # Assigning the runtimes to the lists
        array_times.append(list[i][1])
        snake_loop_times.append(list[i][2])
        loop_times.append(list[i][3])
        slowest_part.append(list[i][4])

    # Finding the slowest measured runtime
    slowest_time = max(max(array_times), max(snake_loop_times), max(loop_times))
    return slowest_time

def timeit_time(filename, Compares = False):
    """Calculates the runtime of given functions using timeit module and
        writes the results to file

    Args:
        filename (str): Filename of the report
        Compares (bool): A variable to extract the runtime using timeit module

    """

    iterations = 3

    # Setting up everything for timeit module to measure runtime for
    # the three functions

    SETUP_CODE1 = '''
from test_slow_rectangle import random_array'''

    TEST_CODE1 = '''
# Generate a random array of size 1e5
array = random_array(1e5)'''

    # timeit.repeat statement
    array_times = timeit.repeat(setup = SETUP_CODE1,
                          stmt = TEST_CODE1,
                          repeat = iterations,
                          number = 1)



    SETUP_CODE2 = '''
from test_slow_rectangle import random_array
from test_slow_rectangle import snake_loop'''

    TEST_CODE2 = '''
# Generate a random array of size 1e5
array = random_array(1e5)
filtered_array = snake_loop(array)'''

    # timeit.repeat statement
    snake_loop_times = timeit.repeat(setup = SETUP_CODE2,
                          stmt = TEST_CODE2,
                          repeat = iterations,
                          number = 1)



    SETUP_CODE3 = '''
from test_slow_rectangle import random_array
from test_slow_rectangle import loop'''


    TEST_CODE3 = '''
# Generate a random array of size 1e5
array = random_array(1e5)
filtered_array_snack = loop(array)'''

    # timeit.repeat statement
    loop_times = timeit.repeat(setup = SETUP_CODE3,
                          stmt = TEST_CODE3,
                          repeat = iterations,
                          number = 1)


    total_time = []
    function_names = ["random_array", "snake_loop", "loop"]

    # Creating the table format to the report
    for i in range(len(loop_times)):
        a = array_times[i]
        b = snake_loop_times[i]
        c = loop_times[i]

        if a > b and a > c:
            d = "array"
        elif b > a and b > c:
            d = "snake_loop"
        else:
            d = "loop"

        t = "Measurement " + str(i+1)
        column = t, a, b, c, d
        total_time.append(column)

    total_time2 = manual_time("manual_report.txt", True) # Extracting manual time
    timeits = round(compare(total_time), 5) # finding the slowest time for timeit
    time = round(compare(total_time2), 5) # finding the slowest time for manual time

    comparison = timeits, time


    if Compares:
        return total_time, total_time2, comparison
    else:
        Write_Results_To_File(filename, function_names, total_time, total_time2, comparison)

if __name__ == '__main__':
    timeit_time("timeit_report.txt") # Writes to file
