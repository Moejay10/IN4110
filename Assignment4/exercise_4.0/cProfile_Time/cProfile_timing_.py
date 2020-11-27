import numpy as np
import cProfile
import pstats
from tabulate import tabulate
import os
import sys

sys.path.append('../')
import test_slow_rectangle as tst
from timeit_Time.timeit_timing_ import timeit_time

def Write_Results_To_File(file, comparison):
    """Writes a report that states the measured time of
        a specific function and compares it with other timing methods.

    Args:
        file (str): The file where the reports is written to
        comparison (list): A list containing the measured time for two other timing methods

    Returns:
        A report in a .txt format containing information of runtimes of a specific function

    """


    file.write(f"The slowest time found by timeit method was {comparison[0]}s \n")
    file.write(f"And by the manual time method the time was {comparison[1]}s \n")
    file.write(f"Compared to cProfile method which is given above in line 3")


    file.close()

def profile_results_To_File(func, func_name, file, filename):
    """Calculates the runtime of given function using cProfile and
        writes the results to file

    Args:
        func (function): A function that converts an image to the gray version of it
        func_name (str): The name of the function that is being timed
        file (str): The file where the reports is written to
        filename (str): Filename of the report

    """

    cProfile.run(func, func_name) # Using cProfile to time function
    profile = pstats.Stats(func_name, stream=file) # Making the results readable
    profile.sort_stats(pstats.SortKey.TIME).print_stats(10) # Printing the results to file

def cProfile_time(filename):
    """Measures the runtime of a specific function and
        compare the results with other time measurements and
        writes the results to file


    Args:
        filename (str): Filename of the report

    """

    if os.path.isfile(filename): # Checking if file exists
        os.remove(filename) # Removes the file


    file = open(filename, 'w')

    profile_results_To_File('tst.snake_loop(tst.random_array(1e5))', 'Function:snake_loop', file, filename)

    manual, timeit, comparison = timeit_time("cProfile_report.txt", True)

    Write_Results_To_File(file, comparison)

if __name__ == '__main__':
    cProfile_time("cProfile_report.txt")
