#!/usr/bin/env python

# importing modules
import datetime
import pandas as pd
import re
import altair as alt
import tempfile
alt.renderers.enable('html')

from functions import read_file, plot_both, plot_reported_cases, plot_cumulative_cases, plot_norway

from flask import Flask
from flask import request 
from flask import render_template

app = Flask(__name__)


@app.route("/")
def start():
    """Get the inital page for the web-server
    
    Return: 
        a rendered template html file
    """ 

    return render_template('layout.html')
 

@app.route("/help")
def help():
    """Get the documentation page created by sphinx
    
    Return: 
        a rendered sphinx_index.html
    """ 

    return render_template('api.html')

@app.route("/norway_plot")
def norway_plot():
    """Plots the map of Norway with the covid data
    
    Return: 
        a rendered template html file
    """ 
   
    fig = plot_norway(False)

    tmp = tempfile.NamedTemporaryFile(suffix=".html")

    fig.save(tmp.name)
    
    with open(tmp.name) as file:
        return file.read()

@app.route("/plot")
def start_plot():
    """Start function for the plot web page
   
   Returns:
        render_template() (function): A function that renders the
            web.html page that loads the plot plage
    """
 
    counties = {
            'agder': 'Agder',
            'innlandet': 'Innlandet',
            'more_romsdal': 'Møre-Romsdal',
            'nordland': 'Nordland',
            'oslo': 'Oslo',
            'rogaland': 'Rogaland',
            'troms_finnmark': 'Troms-Finnmark',
            'trondelag': 'Trøndelag',
            'vestfold_telemark': 'Vestfold-Telemark',
            'vestland': 'Vestland',
            'viken': 'Viken',
            'allCounties': 'All-Counties',
            }

    cases = ['New Cases', 'Cumulative Cases', 'Both']

    reports = ['weekly', 'daily']
    
    return render_template('web.html',
                           name='start',
                           counties=counties.values(),
                           cases=cases,
                           reports=reports)

@app.route('/plot', methods=['POST'])
def show_plots():
    """Start function that is initiated from the plot button, and
        the function responds to POST request. The function takes input from the
        user and plots the data taken from the user on the web page.

    Returns:
        - render_template() (function): A function that renders the
            web.html page that loads the plot page.
    """

    assert request.method == 'POST'  # Checks that the code is in POST request

    counties = {
            'agder': 'Agder',
            'innlandet': 'Innlandet',
            'more_romsdal': 'Møre-Romsdal',
            'nordland': 'Nordland',
            'oslo': 'Oslo',
            'rogaland': 'Rogaland',
            'troms_finnmark': 'Troms-Finnmark',
            'trondelag': 'Trøndelag',
            'vestfold_telemark': 'Vestfold-Telemark',
            'vestland': 'Vestland',
            'viken': 'Viken',
            'allCounties': 'All-Counties',
            }


    cases = ['New Cases', 'Cumulative Cases', 'Both']
    
    reports = ['weekly', 'daily']

    # Access the form data:
    County = str(request.form.get("counties"))
    case = str(request.form.get("cases"))
    report = str(request.form.get("reports"))
    start_date = str(request.form.get("start_date"))
    end_date = str(request.form.get("end_date"))
    
    county = County
    for k, v in counties.items():
        county = re.sub(v, k, County)
        if county != County:
            break


    if start_date == "" or end_date == "":
        daterange = None
        
   
    else:
        daterange = []
        daterange.append(start_date)
        daterange.append(end_date)
    

    
    data = read_file(county, report, daterange)
    
    if case == 'New Cases':    
        fig = plot_reported_cases(County, data, False)

    elif case == 'Cumulative Cases':
        fig = plot_cumulative_cases(County, data, False)

    else:
        fig = plot_both(County, data, False)
    
    
    """
    return render_template('web.html',
                           name='start',
                           counties=counties.values(),
                           cases=cases,
                           reports=reports)
    """ 
    

    tmp = tempfile.NamedTemporaryFile(suffix=".html")

    fig.save(tmp.name)
    
    with open(tmp.name) as file:
        return file.read()
    

if __name__ == '__main__':
    app.run(port=5001, debug=True)
