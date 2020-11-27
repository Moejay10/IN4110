# Exercise 4.1: Gray Filter

## Structure
- Python
  - python_color2gray.py

- Numpy
  - numpy_color2gray.py

- Numba
  - numba_color2gray.py

- Cython
  - cython_color2gray.py
  - cython_color2gray.pyx
  - compile.py
  - compileCython.sh

- functions.py
- grayscale_filter.py

### Packages
The required packages included to run the scripts are:

- numpy
- numba
- cython
- cv2
- os
- time
- tabulate
- datetime
- argparse
- sys

### Execution
You can execute the programs in two ways:

- Method 1

Either directly execute the 4 different implementations of the grayscale image
```
$ python3 python_color2gray.py
```
```
$ python3 numpy_color2gray.py
```
```
$ python3 numba_color2gray.py
```
```
$ python3 cython_color2gray.py
```

And if you execute the scripts directly, a report on the form **script_report_color2gray.txt** is created and the report contains information about time measurements of the program itself and it is also compared to the other implementations.

- Method 2

Or one can run the 4 programs by using the script grayscale_filter.py and execute it by
```
$ python3 grayscale_filter.py
```

#### Remark
To be able to execute the **cython_color2gray.py** directly or use the **grayscale_filter.py** you must first run the script compileCython.sh, to compile the **cython_color2gray.pyx** script.
This can be done in the following way
```
$ ./compileCython.sh
```
And remember to first make the script executable, and this is done by
```
$ chmod a+x compileCython.sh
```
