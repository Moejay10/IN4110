#!/usr/bin/env python

# importing modules
import argparse
import datetime
import pandas as pd
import re
import altair as alt
alt.renderers.enable('altair_viewer')

def main():
    """Tests the implementation of the function get_html

    """
    
    counties = {
            'allCounties': 'All-Counties',
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
            }

    parser = argparse.ArgumentParser(
    description='Reads data from a .csv file and generates a labeled nice plot of date vs. ”number of reported cases” or date vs. ”cumulative number of cases”.',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("-r", "--reports", 
            type=str,
            help='Specifies which reports to be read.',
            choices=['weekly', 'daily'],
            default='daily')


    parser.add_argument("-c", "--county", 
            type=str,
            help='Specifies which county .csv file to be read. Allowed arguments are \n '+',\n '.join(counties.values()),
            metavar='',
            default='All')

    parser.add_argument("-d", "--daterange",
            nargs=2,
            metavar=('Start', 'End'),
            help="The date range to be plotted. \n Example: Start=29/03/2020 End=04/08/2020", 
            default=None) 

    

    args = parser.parse_args()
     
    if args.county == 'All':
        for key, value in counties.items():

            data = read_file(key, args.reports, args.daterange)
            
            plot_norway()

            plot_reported_cases(value, data)

            plot_cumulative_cases(value, data)
    
            plot_both(value, data)
    
    else:
         county = args.county
         for k, v in counties.items():
             county = re.sub(v, k, args.county)
             if county != args.county:
                 break

         data = read_file(county, args.reports, args.daterange)

         plot_norway()

         plot_reported_cases(args.county, data)
         
         plot_cumulative_cases(args.county, data)

         plot_both(args.county, data)
    

def read_file(county, folder="daily", daterange=None):
    """Reads the .csv file and loads the data into a pandas DataFrame.

    Args:
        county (str): The filename of the county to be loaded into a DataFrame.
        folder (str): The folder which contains data from the weekly or daily csv data.
        daterange (list): A list containing the start and end date for the date range specified, otherwise None if nothing specified.
    
    Returns:
        data (DataFrame): The DataFrame of the loaded data which came from the .csv file.
    """


    filename = 'covidData/' + folder + "_reports/" + county + '_reported_cases_covid19t.csv'
    data = pd.read_csv(filename)
    
    if folder == 'daily':
        data['Dato'] = pd.to_datetime(data['Dato'], format='%d.%m.%Y')
    
    else:
        data['Dato'] = pd.to_datetime(data['Dato'] + '-1', format='%Y-%W-%w')

    if daterange != None:
        start_date, end_date = daterange
        # Convert the date in to the iso format
        start_date = re.findall(r'\d{1,2}\/\d{1,2}\/\d{4}', start_date)[0]
        start_date = re.sub(r'(\d{1,2})\/(\d{1,2})\/(\d{4})', '\\3-\\2-\\1', start_date)
        
        end_date = re.findall(r'\d{1,2}\/\d{1,2}\/\d{4}', end_date)[0]
        end_date = re.sub(r'(\d{1,2})\/(\d{1,2})\/(\d{4})', '\\3-\\2-\\1', end_date)
        
        # Select the rows between two dates
        data = data[data["Dato"].isin(pd.date_range(start_date, end_date))]
    
    data = data.rename(columns={'Dato': 'Date', 
        'Kumulativt antall': 'Cumulative number of cases',
        'Nye tilfeller': 'Number of reported cases'})
    
    return data
 
def plot_both(county, data, plot=True):
    """Displays the number of reported cases and cumulative number of cases of
    covid in one plot. That means dual Y-axis. This means one y-axis (right-hand side) will refer to the Number of
    reported cases and the other y-axis (left-hand side) will refer to the Cumulative
    number of cases.

    Args:
        county (str): The name of the county to be plotted. 
        data (DataFrame): The DataFrame of the loaded data which came from the .csv file.

    """

    
    base = alt.Chart(data).transform_fold(
        fold=['Cumulative number of cases', 'Number of reported cases'],
        as_=['Measure', 'Value']
    ).encode(
        x='Date',
        color='Measure:N',
    ).properties(
            title=county + ": Covid-19 cases")

    bar_plot = base.mark_bar().transform_filter(
            alt.datum.Measure == 'Number of reported cases'
    ).encode(
            y='Number of reported cases',
            tooltip=['Date','Number of reported cases'],
    ).interactive()
    
    line_plot = base.mark_line().transform_filter(
            alt.datum.Measure == 'Cumulative number of cases'
    ).encode(
            y='Cumulative number of cases',
            tooltip=['Date','Cumulative number of cases'],
    ).interactive()        


    chart = alt.layer(bar_plot,
            line_plot).resolve_scale(y='independent').properties(width=600, height=600).interactive()
    
    if plot == True:
        chart.show()
    else:
        return chart  
    

    #chart.save('static/' + county + '_both.png')
    

def plot_reported_cases(county, data, plot=True):
    """Plots a bar plot of the data given

    Args:
        county (str): The name of the county to be plotted. 
        data (DataFrame): The input data to be plotted
    """
    
    chart = alt.Chart(data).mark_bar(color='orange').encode(
            x = 'Date',            
            y = 'Number of reported cases',
            tooltip=['Date', 'Number of reported cases'],
    ).interactive().properties(
            title=county + ": Covid-19 cases",
            width=600, height=600).interactive()
    
            
    if plot == True:
        chart.show()
    else:
        return chart

    #chart.save('static/' + county + '_reported_cases.png')
    

def plot_cumulative_cases(county, data, plot=True):
    """Plots a line plot of the data given 
    
    Args:
        county (str): The name of the county to be plotted. 
        data (DataFrame): The input data to be plotted
    """

    chart = alt.Chart(data).mark_line(color='blue').encode(
            x='Date',
            y='Cumulative number of cases',
            tooltip=['Date', 'Cumulative number of cases'],
    ).interactive().properties(
            title=county + ": Covid-19 cases",
            width=600, height=600).interactive()
    
    if plot == True:
        chart.show()
    else:
        return chart

    #chart.save('static/' + county + '_cumulative_cases.png')


def plot_norway(plot=True):
    """Plots the map of Norway where the covid data is highlighted in each county

    Args:
        plot (bool): A bool argument to decide if one shall plot or return figure

    Return:
        figure (altair): Either plots the map of Norway or returns the figure 
    """
    
    # Gets a table of County->Covids infection data
    data = pd.read_csv('covidData/map_reports/map_Norway_covid19.csv')

    # Gets the topojson of norway counties from random github
    counties = alt.topo_feature('https://raw.githubusercontent.com/deldersveld/topojson/master/countries/norway/norway-new-counties.json', 'Fylker')

    
    # Define nearest selection (used for highlighting)
    nearest = alt.selection(type="single", on="mouseover",
            fields=["properties.navn"], empty="none")

    # Plot the map
    fig = alt.Chart(counties).mark_geoshape().encode(
            # Enable hover effect
            tooltip=[
                alt.Tooltip("properties.navn:N", title="County"),
                alt.Tooltip("Insidens:Q", title="Cases per 100K capita"),
            ],
            color=alt.Color("Insidens:Q", scale=alt.Scale(scheme="reds"),
                            legend=alt.Legend(title="Cases per 100K capita")),
            stroke=alt.condition(nearest, alt.value("gray"), alt.value(None)),
            opacity=alt.condition(nearest, alt.value(1), alt.value(0.8)),
    
    # Lookup number of cases from Pandas table and map to counties
    ).transform_lookup(
            lookup="properties.navn",
            from_=alt.LookupData(data, "Category", ["Insidens"])
    ).properties(
            width=600,
            height=600,
            title="Number of cases per 100K in every county",
    ).add_selection(
            nearest
    )
    
    if plot == True:
        fig.show()
    else:
        return fig


if __name__ == '__main__':
    main()
