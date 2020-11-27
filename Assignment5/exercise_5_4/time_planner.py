#!/usr/bin/env python

# importing modules
import argparse
import numpy as np
import requests as req
import datetime
import os
import sys
import re
from bs4 import BeautifulSoup
import pandas as pd


sys.path.append('../')
from exercise_5_1.requesting_urls import get_html

def main():
    """Tests the implementation of the functions extract_events

    """


    parser = argparse.ArgumentParser(
            description='Tests the implementation of the function find_dates.',
            formatter_class=argparse.RawTextHelpFormatter)


    parser.add_argument("-u", "--url", type=str, help="The URL of a given website.", required=True)

    args = parser.parse_args()
    
    output ="betting_slip_empty.md" # Output file for betting slip
    
    new_url, data = get_html(args.url) # Read html text file

    extract_events(data, output)

    
def writeToFile(filename, data):
    """Writes a file containing the webiste text information.

    Args:
        filename (str): The filename of the output text file.
        data (str): The data to be saved to the output file.
        url (str): The response URL of the website.

    """
    
    e = datetime.datetime.now() # Finds the time
    newdir = os.getcwd() + "/datetime_filter/"
    if not os.path.isdir(newdir): # Checking if a path exists
        os.makedirs(newdir) # Creates the path
        filename = newdir + filename

    else:
        filename = os.getcwd() + "/datetime_filter/" + filename

    if os.path.isfile(filename): # Checking if file exists
        os.remove(filename) # Removes the file

    f = open(filename, "a")

    f.write("Date: %s/%s/%s" % (e.day, e.month, e.year))
    f.write("\n")
    f.write("\n")
    
    f.write("BETTING SLIP \n\n")
    
    f.write("Name: \n\n")
    
    f.write(data)

    f.close()



def extract_events(data, output=None):
    """Extracts the data in the date, venue and discipline from the given
    websites

    Args:
        data (str): The html data of the website.
        output (str): The filename of the output text file.

    Return:
        if output is given:
            A output file is written out.
        else:
            the list containing the data is returned.
    """
    soup = BeautifulSoup(data, 'lxml') # Parses the html data 
    
    # Get the table
    all_tables = soup.find_all("table")
    
    # Finds the table with the specific class 
    right_table = soup.find('table', class_='wikitable')
    
    # Converts the table in html into a 2D list
    table = table_to_2d(right_table)
    date = [] 
    venue = []
    discipline = []
    for row in table[1:-1]:
        # Extracts the information from the 2D list
        dis = re.findall(r'[A-Z][A-Z]', row[4])
        d = re.findall(r'(\d{1,2}\s[\w]+\s\d{4})', row[2])
        
        if len(d) == 1:
            date.append(d[0])
        
            venue.append(row[3])
        
            discipline.append(dis[0])

    df=pd.DataFrame(date, columns=['Date'])

    df['Venue'] = venue

    df['Discipline'] = discipline
    
   
    df['Who Wins?'] = "" # Creates an empty coloumn
    
    # Replaces the short disciplines with their full names 
    df['Discipline'] = df['Discipline'].replace(["DH", "SL", "GS", "SG", "AC", "PG"], ["Downhill", "Slalom",
        "Giant Slalom", "Super Giant Slalom", "Alpine Combined", "Parallel Giant Slalom"])
    

    if output is not None:
        data = df.to_markdown(tablefmt="grid") # Creates a markdown table
        writeToFile(output, data)
    
    else:
        return df



from itertools import product

def table_to_2d(table_tag):
    """ Title: How to parse table with rowspan and colspan; source code
    Author: Pieters, Martijn
    Date: 29-03-2019
    Code version: 1.0
    Availability: https://www.iditect.com/how-to/52094811.html """


    rowspans = []  # track pending rowspans
    rows = table_tag.find_all('tr')

    # first scan, see how many columns we need
    colcount = 0
    for r, row in enumerate(rows):
        cells = row.find_all(['td', 'th'], recursive=False)
        # count columns (including spanned).
        # add active rowspans from preceding rows
        # we *ignore* the colspan value on the last cell, to prevent
        # creating 'phantom' columns with no actual cells, only extended
        # colspans. This is achieved by hardcoding the last cell width as 1. 
        # a colspan of 0 means "fill until the end" but can really only apply
        # to the last cell; ignore it elsewhere. 
        colcount = max(
            colcount,
            sum(int(c.get('colspan', 1)) or 1 for c in cells[:-1]) + len(cells[-1:]) + len(rowspans))
        # update rowspan bookkeeping; 0 is a span to the bottom. 
        rowspans += [int(c.get('rowspan', 1)) or len(rows) - r for c in cells]
        rowspans = [s - 1 for s in rowspans if s > 1]

    # it doesn't matter if there are still rowspan numbers 'active'; no extra
    # rows to show in the table means the larger than 1 rowspan numbers in the
    # last table row are ignored.

    # build an empty matrix for all possible cells
    table = [[None] * colcount for row in rows]

    # fill matrix from row data
    rowspans = {}  # track pending rowspans, column number mapping to count
    for row, row_elem in enumerate(rows):
        span_offset = 0  # how many columns are skipped due to row and colspans 
        for col, cell in enumerate(row_elem.find_all(['td', 'th'], recursive=False)):
            # adjust for preceding row and colspans
            col += span_offset
            while rowspans.get(col, 0):
                span_offset += 1
                col += 1

            # fill table data
            rowspan = rowspans[col] = int(cell.get('rowspan', 1)) or len(rows) - row
            colspan = int(cell.get('colspan', 1)) or colcount - col
            # next column is offset by the colspan
            span_offset += colspan - 1
            value = cell.get_text()
            for drow, dcol in product(range(rowspan), range(colspan)):
                try:
                    table[row + drow][col + dcol] = value
                    rowspans[col + dcol] = rowspan
                except IndexError:
                    # rowspan or colspan outside the confines of the table
                    pass

        # update rowspan bookkeeping
        rowspans = {c: s - 1 for c, s in rowspans.items() if s > 1}

    return table


if __name__ == '__main__':
    main()

