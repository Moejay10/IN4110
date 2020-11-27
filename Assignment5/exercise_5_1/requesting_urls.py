#!/usr/bin/env python

# importing modules
import argparse
import numpy as np
import requests as req
import datetime
import os

def get_html(url, params=None, output=None):
    """Makes a URL request and retrieves html data of a given website. Moreover, it saves the response URL and tex          t to a text file. 

    Args:
        url (str): The URL of the website of choice.
        params: (dic): A dictionary containing data that will be given as key/value pair in the URL.
        output (str): Filename of the output text file.

    Returns:
        If the optional argument of the output text file is set:
            output (str): The filename of the output text file containing the response URL and text.
        Otherwise:
            response (str): The URL is returned. 
    """
    # grabbing the content of url-link
    if params == None: 
        resp = req.get(url) # get() method returns a response object
    else:
        resp = req.get(url, params=params) # get() method returns a response object
    
    # If no output is given the html data from the webiste is returned 
    if output == None:
        return resp.url, resp.text
    else:
        writeToFile(output, resp.text, resp.url)



def writeToFile(filename, data, url):
    """Writes a file containing the webiste text information.

    Args:
        filename (str): The filename of the output text file.
        data (str): The data to be saved to the output file.
        url (str): The response URL of the website.

    """
    # Finds the time the program last ran 
    e = datetime.datetime.now() # Finds the time
    newdir = os.getcwd() + "/requesting_urls/"
    if not os.path.isdir(newdir): # Checking if the path exists
        os.makedirs(newdir) # Creates the path
        filename = newdir + filename

    else:
        filename = os.getcwd() + "/requesting_urls/" + filename

    if os.path.isfile(filename): # Checking if file exists
        os.remove(filename) # Removes the file

    f = open(filename, "a")

    f.write(f"Last run date was %s/%s/%s at %s:%s:%s \n" % (e.day, e.month, e.year, e.hour, e.minute, e.second ))
    f.write("\n")
    f.write("\n")
    f.write("#--------------------------------------------------------------------------#")
    f.write("\n")
    f.write("\n")
    
    f.write(data)

    f.close()


def main():
    """Tests the implementation of the function get_html

    """


    parser = argparse.ArgumentParser(
    description='Tests the implementation of the function get_html.',
    formatter_class=argparse.RawTextHelpFormatter
    )


    parser.add_argument("-u", "--url", type=str, help="The URL of a given website.", required=True)

    parser.add_argument("-k", "--keys", type=str, nargs='+', help="The key arguments in the URL. Example '-k key_1 key_2 ... key_n'.", default=None)

    parser.add_argument("-v", "--values", type=str, nargs='+', help="The values arguments in the URL. Example '-v -value_1 value_2 ... value_n'.", default=None)
    
    parser.add_argument("-o", "--output", type=str, help="The optional output filename.", default=None)

    args = parser.parse_args()

        
    if args.keys == args.values == None:
        params = None

    else:

        if len(args.keys) != len(args.values):
            raise ValueError("The number of keys and values arguments does not fit. The same number of arguments must be given")

        params = {}
        for i in range(len(args.keys)):
            params[args.keys[i]] = args.values[i]
        
    get_html(args.url, params, args.output)     



if __name__ == '__main__':
    main()
