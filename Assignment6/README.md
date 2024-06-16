# Assignment 6 - Web Programming & Data Analysis 
In this assignment, we built a web-based visualization of
the corona dataset made publicly available by Folkehelseinstituttet (FHI).
The data can be found on the following website https://www.fhi.no/sv/smittsomme-sykdommer/corona/dags--og-ukerapporter/dags--og-ukerapporter-om-koronavirus/.


## Structure
- docs
  - source
    - functions.py
    - web_visualization.py
    - static
    - covidData
    - templates

## Packages
The required packages included to run the Python scripts are:

- argparse
- datetime
- pandas
- regex
- tempfile
- altair
- flask

## Visualization through a web app
The script web_visualization.py uses the programs developed in functions.py and
the Flask module to run a simple web-interface showing the plots of the corona
dataset.

### Execution
Executing the the script is done by:
```
$ python3 web_visualization.py 
```
You should then be able to go to the localhost:5001 in your browser.
To close the server press **ctrl + c**.



