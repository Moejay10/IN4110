# Assignment 3 - Basic Python Programming

## Exercise 3.1: Word Counter
This script can take a file(s) and will count the amount of lines, words and characters there is in the file.

### Packages
The required packages included to run the program are:

- os
- pathlib
- tabulate

### Execution
You execute the program by:

```
$ python3 wc.py filename.txt
```

To execute the program with multiple files can be done by:

```
$ python3 wc.py filename1.txt filename2.txt filename3.txt ... filenameN.txt
```

To execute the program for all files in the current directory can be done by:

```
$ python3 wc.py "*"
```

And to execute the program for all file of a specific type in the current directory, ie. .py files, can be done by:

```
$ python3 wc.py "*.py"
```

## Exercise 3.2 - 3.5: Arrays
The script test_array confirms that the script Array works as expected.

### Packages
The required packages included to run the programs are:

- unittest
- numpy

**Note:** The tests in test_Array was implemented with pytest.

### Execution
To run the tests you must install **pytest**.

Executing the tests is done by:

```
$ pytest
```
