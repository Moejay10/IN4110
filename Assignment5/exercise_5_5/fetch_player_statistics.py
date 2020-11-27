#!/usr/bin/env python

# importing modules
import numpy as np
import matplotlib.pyplot as plt
import requests as req
import os
import sys
import re
from bs4 import BeautifulSoup
import pandas as pd
import random

sys.path.append('../')
from exercise_5_1.requesting_urls import get_html
from exercise_5_4.time_planner import table_to_2d
from exercise_5_2.filter_urls import find_articles, find_urls

def main():
    """Visits the the 2020 NBA playoffs wikipedia website and plots player
    statistics.

    """
    
    url = 'https://en.wikipedia.org/wiki/2020_NBA_playoffs' 
    new_url, data = get_html(url) # Read html text file
    
    plot_stats(data)
    


def extract_teams(data):
    """Extracts the table from the website using BeautifulSoup

    Args:
        data (str): The html data from the given website.
        
    Return:
        tables[0] (list): A list containing the information about the html
        table of the teams.
        round_teams (list): A list containing the teams.
    """
    
    soup = BeautifulSoup(data, 'lxml') # Parses the html data
    # Extract the tag that defines the header just before our table of interest
    title = soup.find(id="Bracket")
    # Extracts all the following table tags
    tables = title.find_all_next("table")
    
    # Converts the html table into a 2D list
    table = table_to_2d(tables[0])
    new_table = list(zip(*table)) # Transposes the list
     
    list_count1 = 0
    list_count2 = 0
    for rows in new_table:
        if rows[0] == 'Conference Semifinals' + "\n":
            list_count1 += 1
            if list_count1 == 2:
                round_teams = list(dict.fromkeys(list(rows)))
                
                # Removes unwanted characters in the string
                round_teams.remove('Eastern Conference\n')
                round_teams.remove('Western Conference\n')
                round_teams.remove('\n')
                round_teams.remove(None)
                round_teams.remove('\xa0\n')

                for i in range(len(round_teams)):
                    # Removes unwanted characters and spaces in string
                    round_teams[i] = round_teams[i].strip()
                    round_teams[i] = round_teams[i].strip('*')

    for i in range(len(round_teams)):
        # Replaces a specific string with empty space
        round_teams[i] = round_teams[i].replace("LA ", "")

    return tables[0], round_teams
    

def extract_url(data):
    """Extracts the team urls in a given table

    Args:
        data (str): The html data from the given website.

    Return:
        team_urls (list): A list containing the links of all the teams.
        semifinal_teams (list): A list containing the teams.
    """
    
    table, semifinal_teams = extract_teams(data)
    wiki = find_articles(str(table)) # Finds all the wikipedia links of the teams
    wiki = list(dict.fromkeys(wiki)) # Removes all duplicate elements
    wiki = '\n'.join(wiki) # Creates spaces between each list element
    team_urls = []
    
    for team in semifinal_teams:
        # Extracts all the team urls
        regex = '^(https:\/\/en\.[\w]+\.[\w]+\/wiki\/\d{4}%[\w]+%\d{2}%\d{4}_(Los_Angeles_)?' + team + '[\w]+)$' 
         
        temp = re.findall(regex, wiki, re.M)
        if temp != []:
            for t in temp:    
                team_urls.append(''.join(t[0]))
    
    
    return team_urls, semifinal_teams


def extract_player(data):
    """Extracts the players from each team found in extract_url.
    
    Args:
        data (str): The html data from the given website.

    Return:
        player_names (list): A list containing the names og all the players
        teams (list): A list containing the teams of the playoffs.
        wiki (list): A list containing the links for all the players wiki
        website.
    """

    team_urls, teams = extract_url(data)
    wiki = []
    player_names = []
    for team in team_urls:
        new_url, new_data = get_html(team)
    
        soup = BeautifulSoup(new_data, 'lxml') # Parses html data
        title = soup.find(id="Roster") # Locates html data with specific id
        tables = title.find_all_next("table") # Finds a specific table

        table = table_to_2d(tables[0]) # Converts the html table into a 2D list
        player_name = [] 
        for row in table:
            # Extracts all player names in the roster of the team
            player_name.append(row[2])
            if player_name[-1] == None or player_name[-1] == 'Name':
                player_name.pop(-1)
            
            
        for i in range(len(player_name)):
            # Removes all unwanted characters in the player names
            player_name[i] = player_name[i].strip()
            player_name[i] = player_name[i].replace("(TW)", "")
            player_name[i] = player_name[i].replace("(C)", "")
            
            a = player_name[i]
            
            # Creates the link of each player from their names
            a = a.split(', ')
            b = a[1].replace(" ", "_")
            c = b +  "_" + a[0]
            # Adds base url each player name and creates link to each player website
            link = "https://en.wikipedia.org/wiki/" + c

            wiki.append(link)
            player_names.append(player_name[i])
        

    return player_names, teams, wiki


def extract_stats(data):
    """Extracts the player statistics from their wikipedia page

    Args:
        data (str): The html data from the NBA playoffs 2020 wikipedia page.

    Return:
        team_stats (list): A list containing the stats for all teams.
        teams (list): A list containing all the teams in the playoffs.
        
    """
    player_names, teams, wiki = extract_player(data)

    
    for i in range(len(teams)):
        # Replaces specific string with another string
        teams[i] = teams[i].replace("Clippers", "L.A. Clippers")
        teams[i] = teams[i].replace("Lakers", "L.A. Lakers")
        
    stats = pd.DataFrame()
    

    for i in range(len(wiki)):
        
        try:
            new_url, new_data = get_html(wiki[i]) # Gets html data from url
            soup = BeautifulSoup(new_data, 'lxml') # Parses html data
            title = soup.find(id="Regular_season") # Locates specific tag in html data
            
            if title != None: # Checks if players website has correct id for table
                tables = title.find_all_next("table") # Locates specific table in html data

        except AttributeError: 
            # Players with common names which needs specific tag for link  
            link2 = wiki[i] + "_(basketball)"
            new_url, new_data = get_html(link2) # Gets html data from url
            soup = BeautifulSoup(new_data, 'lxml') # Parses html data
            title = soup.find(id="Regular_season") # Locates specific tag in html data
            
            if title != None: # Checks if players website has correct id for table
                tables = title.find_all_next("table") # Locates specific table in html data

        player = player_names[i]          
        table = table_to_2d(tables[0]) # Converts html table data into 2D list
        
        for row in table:
            # Finds the specific row with the statistics 
            a = row[0].strip()
            a = list(''.join(a))
            b = a[-3] + a[-2]
            c = a[-2] + a[-1]

            # Checks to see if the statistics is in the year 2019-2020
            if b == '20' or c == '20':
                team = row[1].strip() # Collects team name
                if team in teams[1:]:
                    # Removes unwanted characters and extracts stats from players website
                    player = player.replace("\xa0", "")
                    ppg = row[-1].strip()
                    ppg = ppg.replace("*", "")
                    ppg = ppg.replace("-", "0")

                    bpg = row[-2].strip()
                    bpg = bpg.replace("*", "")
                    bpg = bpg.replace("-", "0")

                    rpg = row[-5].strip()
                    rpg = rpg.replace("*", "") 
                    rpg = rpg.replace("-", "0")


                    dic = {'Team': team, 'Player': player, 'PPG': float(ppg), 'BPG': float(bpg), 'RPG': float(rpg)}
                    stats = stats.append(dic, ignore_index=True) 
       
    
    team_stats = []
    
    for team in teams[1:]:
        # Creates a dictionary for each team with their player stats
        stat = stats[stats['Team'] == team]
        stat = stat.sort_values('PPG', ascending=False)
        stat = stat.reindex(columns=['Team', 'Player', 'PPG', 'BPG', 'RPG'])
        team_stats.append(stat)


    return team_stats, teams[1:]


def plot_stats(data):
    """Plots the extracted statistics for the NBA conference semifinal teams 

    Args: 
        data (str): The html data from the NBA playoffs 2020 wikipedia page
    """
    # Creates the specific folder if its not already there 
    newdir = os.getcwd() + "/NBA_player_statistics/"
    if not os.path.isdir(newdir):
        os.makedirs(newdir)



    team_stats, teams = extract_stats(data)
    
    for i in range(len(teams)):
        # Replaces strings
        teams[i] = teams[i].replace("L.A. Clippers", "Clippers")
        teams[i] = teams[i].replace("L.A. Lakers", "Lakers")
     
    import seaborn as sns
    sns.set()
    
    player = []

    ppg1 = []
    ppg2 = []
    ppg3 = []
    
    bpg1 = []
    bpg2 = []
    bpg3 = []
    
    rpg1 = []
    rpg2 = []
    rpg3 = []
    
    # Goes through each team and their stats
    for i in range(len(team_stats)):
        stats = team_stats[i]
        team = teams[i]
        # Extracts all the data for plotting and putting them in a list
        player.append(stats['Player'].values[0])
        player.append(stats['Player'].values[1])
        player.append(stats['Player'].values[2])
        
        ppg1.append(stats['PPG'].values[0])
        ppg2.append(stats['PPG'].values[1])
        ppg3.append(stats['PPG'].values[2])

        bpg1.append(stats['BPG'].values[0])
        bpg2.append(stats['BPG'].values[1])
        bpg3.append(stats['BPG'].values[2])

        rpg1.append(stats['RPG'].values[0])
        rpg2.append(stats['RPG'].values[1])
        rpg3.append(stats['RPG'].values[2])

    
    X = np.arange(len(teams))
    bars1 = X
    bars2 = X + 0.25
    bars3 = X + 0.5
    # Creates the lists to plot player names over each bar chart
    bars4 = list(bars1) + list(bars2) + list(bars3)
    r4 = ppg1 + ppg2 + ppg3
    
    fig = plt.figure(figsize=(10,7)) # Chooses the fig size of the plot 
    plt.bar(bars1, ppg1, color = 'b', width = 0.25)
    plt.bar(bars2, ppg2, color = 'r', width = 0.25)
    plt.bar(bars3, ppg3, color = 'g', width = 0.25)
    plt.legend(["1st Ranked Player in the Team", "2nd Ranked Player in the Team", "3rd Ranked Player in the Team"])
    # Adding Xticks
    barWidth = 0.25 # The width of the barchart
    plt.xlabel('Teams', fontweight ='bold')
    plt.ylabel('Points per Game', fontweight ='bold')
    # Creates the team name on the x-axis
    plt.xticks([r + barWidth for r in range(len(ppg1))], teams)
    # Creates the text over the bar chart 
    for i in range(len(player)):
        plt.annotate(player[i], (bars4[i], r4[i]), size=7, weight = 'bold', rotation = 90)
    
    fig.savefig(newdir + 'players_over_ppg.png')
    plt.show()

    fig = plt.figure(figsize=(10,7))
    plt.bar(bars1, bpg1, color = 'b', width = 0.25)
    plt.bar(bars2, bpg2, color = 'g', width = 0.25)
    plt.bar(bars3, bpg3, color = 'r', width = 0.25)
    plt.legend(["1st Ranked Player in the Team", "2nd Ranked Player in the Team", "3rd Ranked Player in the Team"])

    # Adding Xticks
    plt.xlabel('Teams', fontweight ='bold')
    plt.ylabel('Blocks per Game', fontweight ='bold')
    plt.xticks([r + barWidth for r in range(len(bpg1))], teams)
    
    r4 = bpg1 + bpg2 + bpg3
    # Creates the text over the bar chart 
    for i in range(len(player)):
        plt.annotate(player[i], (bars4[i], r4[i]), size=7, weight = 'bold', rotation = 90)
    
    
    fig.savefig(newdir + 'players_over_bpg.png')
    plt.show()

    fig = plt.figure(figsize=(10,7))
    plt.bar(bars1, rpg1, color = 'b', width = 0.25)
    plt.bar(bars2, rpg2, color = 'g', width = 0.25)
    plt.bar(bars3, rpg3, color = 'r', width = 0.25)
    plt.legend(["1st Ranked Player in the Team", "2nd Ranked Player in the Team", "3rd Ranked Player in the Team"])

    # Adding Xticks
    plt.xlabel('Teams', fontweight ='bold')
    plt.ylabel('Rebounds per Game', fontweight ='bold')
    plt.xticks([r + barWidth for r in range(len(rpg1))], teams)
    
    r4 = rpg1 + rpg2 + rpg3
    # Creates the text over the bar chart 
    for i in range(len(player)):
        plt.annotate(player[i], (bars4[i], r4[i]), size=7, weight = 'bold', rotation = 90)

    
    fig.savefig(newdir + 'players_over_rpg.png')
    plt.show()



if __name__ == '__main__':
    main()
