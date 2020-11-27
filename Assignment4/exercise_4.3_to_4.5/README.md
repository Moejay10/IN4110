# Exercise 4.3 - 4.5: Instapy Package

## Structure
- bin
  - instapy (User interface script)

- instapy (Package Folder)
  - gray
    - python_color2gray.py
    - numpy_color2gray.py
    - numba_color2gray.py
    - cython_color2gray.pyx

  - sepia
  - python_color2sepia.py
  - numpy_color2sepia.py
  - numba_color2sepia.py
  - cython_color2sepia.pyx

  - functions.py
  - grayscale_image.py
  - sepia_image.py

- setup.py (Script to install package)

- test_instapy (Unit tests)

## Packages
The required packages included to run the Python scripts are:

- numpy
- numba
- cython
- cv2
- os
- argparse
- distutils
- random

## Installation
One can install the package by:
```
$ pip3 install -e .
```

To install the package on an IFI machine:

```
$ pip3 install -e . --user
```

## Execution
You can execute the program by:
```
$ instapy
```
If you are running the package on a machine you do not have root access you will need to create a virtual environment first and then the script should be available system wide.
This can be done by:

- Create virtual environment
```
$ python3 -m venv /path/to/new/virtual/environment
```

- Go inside the newly created virtual environment
```
$ cd /path/to/new/virtual/environment
```

- Activate the virtual environment
```
$ source bin/activate
```
Then the name of the environment starts showing up inside parentheses to indicate that we are now working inside the environment.

- Deactivate virtual environment
```
$ deactivate
```

For more information on these read these references:
- https://docs.python.org/3/library/venv.html
- https://towardsdatascience.com/python-virtual-environments-made-easy-fe0c603fe601


To run the tests you must install **pytest**.
The tests can be found in the script test_instapy.py

Executing the tests is done by:

```
$ pytest
```
