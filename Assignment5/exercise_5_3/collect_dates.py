#!/usr/bin/env python

# importing modules
import argparse
import numpy as np
import requests as req
import os
import sys
import re
import pandas as pd
import datetime

sys.path.append('../')
from exercise_5_1.requesting_urls import get_html

def main():
    """Tests the implementation of the functions find_dates

    """


    parser = argparse.ArgumentParser(
            description='Tests the implementation of the function find_dates.',
            formatter_class=argparse.RawTextHelpFormatter)


    parser.add_argument("-u", "--url", type=str, help="The URL of a given website.", required=True)

    parser.add_argument("-o", "--output", type=str, help="The optional output filename.", default=None)

    args = parser.parse_args()
    
    new_url, data = get_html(args.url) # Read html text file
    
    # Finds all dates from the given website
    dates = find_dates(data)
    
    find_dates(data, args.output)

def find_dates(data, output=None):
    """Finds the dates in a body of html using regex.

    Args:
        data (str): A string of html.

    Returns:
        dates (list): A list of all dates found in the html.
    """
    total_dates = []
    
    # Finds all dates on the form YYYY-MM-DD
    iso = re.findall(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))',data)
    
    for i in range(len(iso)):
        iso[i] = iso[i][0] 
        iso[i] = ''.join(iso[i]) # Converting into a string 
        # Converting into format yyyy/mm/dd
        iso[i] = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\1/\\2/\\3', iso[i]) 

        total_dates.append(iso[i])
    
    
    
    month_numbers = {r'Jan(uary)?': '01', r'Feb(ruary)?': '02',
            r'Mar(ch)?': '03',
            r'Apr(il)?': '04', r'May': '05',
            r'Jun(e)?': '06', r'Jul(y)?': '07', r'Aug(ust)?': '08',
            r'Sep(tember)?': '09',
            r'Oct(ober)?': '10',
            r'Nov(ember)?': '11', r'Dec(ember)?': '12'}

    # Finds all the dates on the form "Month day, Year" and "Month, Year"  
    mdy = re.findall(r'((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember){2,8}?))(\s\d{2})?,(\s[12][0-9]{3})', data)
    for m in range(len(mdy)):
        mdy[m] = ''.join(mdy[m])
        # Converting into format yyyy/mm/dd
        mdy[m] = re.sub(r'([\w]+)\s(\d{1,2})\s?(\d{4})', '\\3/\\1/\\2', mdy[m]) 
        
        # Substitutes month name with corresponding month number
        for k, v in month_numbers.items():
            mdy[m] = re.sub(k, v, mdy[m])
        
        total_dates.append(mdy[m])

    # Finds all the dates on the form "Day Month Year" and "Month Year" 
    dmy = re.findall(r'(\d{2}\s)?((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember){2,8}?))(\s[12][0-9]{3})', data)

    for d in range(len(dmy)):
        dmy[d] = ''.join(dmy[d]) # Converting into a string
        
        # Converting into format yyyy/mm/dd
        dmy[d] = re.sub(r'(\d{1,2})?\s?([\w]+)\s(\d{4})', '\\3/\\2/\\1', dmy[d]) 
        
        # Substitutes month name with corresponding month number
        for k, v in month_numbers.items():
            dmy[d] = re.sub(k, v, dmy[d])
        
        
        total_dates.append(dmy[d]) 
 
    
    # Finds all the dates on the form "Year Month Day" 
    ymd = re.findall(r'([12][0-9]{3}\s)((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember){2,8}?)\s)(\d{2})?', data)
    
    for y in range(len(ymd)):
        ymd[y] = ''.join(ymd[y]) # Converting into a string
        # Converting into format yyyy/mm/dd
        ymd[y] = re.sub(r'(\d{4})\s([\w]+)\s(\d{1,2})', '\\1/\\2/\\3', ymd[y])

        # Substitutes month name with corresponding month number
        for k, v in month_numbers.items():
            ymd[y] = re.sub(k, v, ymd[y])
           

        total_dates.append(ymd[y])
    
    # Sort the list in ascending order of dates
    total_dates = sorted(total_dates)
   
    if output == None:
       return total_dates
    
    else:
        writeToFile(output, total_dates)

def writeToFile(filename, data):
    """Writes a file containing the urls found in a given website.

    Args:
        filename (str): The filename of the output text file.
        data1 (str): Data containing all the urls found in a given website.
        data2 (str): Data containing all the wikipedia articles found in the given website.

    """
    # Converts the lists into a string, where each list element starts on a new line
    data = '\n'.join(data)

    e = datetime.datetime.now() # Finds the time
    newdir = os.getcwd() + "/filter_dates_regex/"
    if not os.path.isdir(newdir):
        os.makedirs(newdir)
        filename = newdir + filename

    else:
        filename = os.getcwd() + "/filter_dates_regex/" + filename

    if os.path.isfile(filename): # Checking if file exists
        os.remove(filename) # Removes the file
    
    f = open(filename, "a")

    f.write(f"Last run date was %s/%s/%s at %s:%s:%s \n" % (e.day, e.month, e.year, e.hour, e.minute, e.second ))
    f.write("\n")
    f.write("\n")
    f.write("#--------------------------------------------------------------------------#")
    f.write("\n")
    f.write("\n")
    
    f.write('All dates in the url\n')
    f.write("--------------\n")

    f.write(data)

    f.write("\n")
    f.write("\n")
    f.write("#--------------------------------------------------------------------------#")

    f.close()  
    

if __name__ == '__main__':
    main()
