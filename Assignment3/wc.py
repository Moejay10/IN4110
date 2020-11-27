#!/usr/bin/env python
import sys
import os
from pathlib import Path
from tabulate import tabulate

def files_exist(file_list):
    """
    files_exist: Checks to see if a file exists in the current directory.

    Args:
        filename (string): Filename that the function shall verify exists in the current directory.
    """

    file_found = [] # Creates empty list
    for item in file_list:
        if os.path.isfile(item): # Checking to see if file exists
            file_found.append(item)
    return file_found


def readfiles(filename):
    """
    readfiles: goes through the file and counts the lines, words and characters in a file.

    Args:
        filename (string): Filename that the function shall count lines, words and characters.
    """

    table = [] # Createss empty list

    for file in filename:
        list_a = [] # Is the number of lines in the file
        list_b = [] # Is the number of words in the file
        list_c = [] # Is the number of characters in the file
        with open(file, "rb") as f:
            lines = f.readlines() # Reads file
            for line in lines: # Goes through file, line for line
                list_a.append(line) # Adds each line to the list
                words = line.split() # Splits line
                for word in words: # Goes through file, words in each line
                    list_b.append(word) # Adds each word in a line to the list
                    for characters in word: # Goes through file, characters in each word
                        list_c.append(characters) # Adds each characters in a word to the list

        a = len(list_a) # Counts the total number of lines in the file
        b = len(list_b) # Counts the total number of word in the file
        c = len(list_c) # Counts the total number of characters in the file

        column = file, a, b, c
        table.append(column)
    # Prints the values in a nice tabulated form
    print(tabulate((table), headers=['Filename', 'Number of lines:',
    'Number of words:', 'Number of characters:'], tablefmt='orgtbl'))

def main():
    """
    main: Depending on input, gives error message or calls above functions.
    """

    fn = sys.argv[1:] # Is the filename or all files in the directory

    if len(fn) < 1: # Checking if any command line argument was given
        print("No command line argument given. Valid arguments are: filename, '*' or '*.filetype' ")

    elif sys.argv[1] == "*":
        listOfFiles = [] # Creates empty list
        for root, dirs, files in os.walk("."): # Goes through files in the working directory
            for filename in files:
                listOfFiles.append(os.path.join(root,filename)) # Adds all files in the working directory to a list

        readfiles(listOfFiles) # Going through file and counts line, words and characters

    elif len(fn) == 1: # Checking if only one command line argument was given

        end_filetype = list(sys.argv[1])
        end = ""
        for symbol in end_filetype:
            if symbol != end_filetype[0]:
                end += str(symbol)

        if any( (file.endswith(end)) for file in os.listdir() ):# Checking if file ends with a specific file type
            listOfFiles = []
            for root, dirs, files in os.walk("."): # Goes through files in the working directory
                for filename in files:
                    if filename.endswith(end): # Finding all files with specific file type
                        listOfFiles.append(os.path.join(root,filename))

            readfiles(listOfFiles) # Going through file and counts line, words and characters

        else:
            print("Not valid command line argument given. Valid arguments are: filename, '*' or '*.filetype' ")

    elif len(fn) >= 1: # Checking if one or more file is given as command line arguments
        listOfFiles = files_exist(fn)
        if any(listOfFiles) == True:
            readfiles(listOfFiles) # Going through file and counts line, words and characters

        else:
            print("Not valid command line argument given. Valid arguments are: filename, '*' or '*.filetype' ")

    else:
        print("Not valid command line argument given. Valid arguments are: filename, '*' or '*.filetype' ")


main()
