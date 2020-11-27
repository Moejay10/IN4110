# Exercise 4.0: Profiling

## Structure
- manual_Time
  - manual_timing_.py

- timeit_Time
  - timeit_timing_.py

- cProfile_Time
  - cProfile_timing_.py

- test_slow_rectangle.py

### Packages
The required packages included to run the Python scripts are:

- numpy
- os
- time
- timeit
- cProfile
- pstats
- tabulate
- sys
- matplotlib

### Execution
You execute the programs by:

```
$ python3 script_timing_.py
```
where **script** is one of the three Python scripts mentioned above.

And for each of the programs, when you run on one of them, a report on the form 'script_report.txt' is created with information about time measurements of the script test_slow_rectangle.py.

#### Disclaimer
To be able to run the script **cProfile_timing_.py** one needs Python 3.7 version.
