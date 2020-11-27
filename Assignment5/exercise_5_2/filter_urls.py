#!/usr/bin/env python

# import the modules
import numpy as np
import argparse
import requests as req
import re
import datetime
import os
import sys

sys.path.append('../')
from exercise_5_1.requesting_urls import get_html

def main():
    """Tests the implementation of the functions find_urls and find_articles

    """


    parser = argparse.ArgumentParser(
            description='Tests the implementation of the function find_urls and find_articles.',
            formatter_class=argparse.RawTextHelpFormatter)


    parser.add_argument("-u", "--url", type=str, help="The URL of a given website.", required=True)

    parser.add_argument("-o", "--output", type=str, help="The optional output filename.", default=None)

    args = parser.parse_args()
    
    new_url, data = get_html(args.url) # Read html text file
    
    # Finds all Wikipedia articles from the given website
    find_articles(data, args.output) 
     


def find_urls(data):
    """Receives a string of html and returns a list of all urls found in the text.

    Args:
        data (str): Containts the string of html.

    Returns
        links (list): A list of all urls found in the text. 

    """

    # Use re.findall to get all the links in the html file that starts with a '#'
    unwanted = re.findall(r'href=[\'"]?#([^\'" >]+)', data)
    # Use re.findall to get all the links in the html file
    links = re.findall(r'href=[\'"]?([^#\'">]+)', data)

    for i in range(len(unwanted)):
        unwanted[i] = "#" + unwanted[i]
    
    # Removes all urls that start with the '#'
    links = [ele for ele in links if ele not in unwanted] 

    return links

def find_articles(data, output=None):
    """Receives a string of html and returns a list of all Wikipedia articles found in the text.

    Args:
        data (str): Containts the string of html.

    Returns:
        If the optional argument of the output text file is set:
            output (str): The filename of the output text file containing the
            all urls and all Wikipedia articles found in the given website.
        Otherwise:
            wiki (list): A list of all Wikipedia articles found in the text. 

    """

    # Converts the list into a string, where each list element starts on a new line
    link = find_urls(data) # Contains all the urls in the html file
    links = '\n'.join(link) 
    
    wiki = []
    # Finds all the relative wiki links that in every line starts as '\wiki\'
    wiki1 = re.findall(r'^(\/)(wiki)(\/)([\w\%]+)', links, flags=re.M) 
    # re.M is regex flag that tells re.findall to look in multilines

    # Finds all the wiki links that start with their base url
    wiki2 = re.findall(r'(http)(s)?(:)?(\/)(\/)([\w]+)(\.)(wikipedia)(\.)([\w]+)(\/)([\w]+)(\/)([\w%]+)', links)
    for i in range(len(wiki1)):
        wiki1[i] = ''.join(wiki1[i]) # Converting into a string
        # Adding base url to the relative urls
        wiki1[i] = "https://en.wikipedia.org" + wiki1[i] # Adds base url to relative urls
        wiki.append(wiki1[i])
        

    for i in range(len(wiki2)):
        wiki2[i] = ''.join(wiki2[i]) # Converting into a string
        wiki.append(wiki2[i])
    
    if output == None:
        return wiki
    else:
        writeToFile(output, link, wiki)

def writeToFile(filename, data1, data2):
    """Writes a file containing the urls found in a given website.

    Args:
        filename (str): The filename of the output text file.
        data1 (str): Data containing all the urls found in a given website.
        data2 (str): Data containing all the wikipedia articles found in the given website.

    """
    # Converts the lists into a string, where each list element starts on a new line
    data1 = '\n'.join(data1) 
    data2 = '\n'.join(data2)

    e = datetime.datetime.now() # Finds the time
    newdir = os.getcwd() + "/filter_urls/"
    if not os.path.isdir(newdir): # Checking if path exists
        os.makedirs(newdir) # Creates path
        filename = newdir + filename

    else:
        filename = os.getcwd() + "/filter_urls/" + filename

    if os.path.isfile(filename): # Checking if file exists
        os.remove(filename) # Removes the file
    
    f = open(filename, "a")

    f.write(f"Last run date was %s/%s/%s at %s:%s:%s \n" % (e.day, e.month, e.year, e.hour, e.minute, e.second ))
    f.write("\n")
    f.write("\n")
    f.write("#--------------------------------------------------------------------------#")
    f.write("\n")
    f.write("\n")
    
    f.write('All url links\n')
    f.write("--------------\n")

    f.write(data1)

    f.write("\n")
    f.write("\n")
    f.write("#--------------------------------------------------------------------------#")
    f.write("\n")
    f.write("\n")
    
    f.write('Wikipedia articles\n')
    f.write("-------------------\n")

    f.write(data2)

    f.close()  
    

if __name__ == '__main__':
    main()
