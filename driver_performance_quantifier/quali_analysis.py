import fastf1
from fastf1 import plotting as f1plt
import pandas as pd
import numpy as np
import json
from datetime import timedelta as td # Specifically to normalize timedelta to float. Probably a better solution somewhere in pandas or nmpy

drivers = {} # driver : { 'name' : "NAME", 'team' : "TEAM", 'results' : [], 'delta' : [] }

SESSION_TYPE = 'Q'
year = 2025

# Do the first round on its own for full understanding of how it will work, then put into a loop to go from round 2->24
round = 1


session = fastf1.get_session(year, round, SESSION_TYPE)
session.load()

# Load the drivers from data_frame if they arent in
results = session.results
for idx, row in results.iterrows():
    the_driver = row['Abbreviation']
    if the_driver not in drivers:
        drivers[the_driver] = { 'name' : row['FullName'], 'team' : row['TeamName'], 'results' : [], 'delta' : [] }
    # Driver has all fields

for team, team_data in results.groupby("TeamName"):
    if len(team_data) < 2:
        continue  # skip incomplete teams
    driver1 = team_data.iloc[0]
    driver2 = team_data.iloc[1]

    # This is inefficient but whatever, it only needs to run once*
    if pd.notna(driver1.Q3) and pd.notna(driver2.Q3):
        d1_time = driver1.Q3/td(seconds=1)
        d2_time = driver2.Q3/td(seconds=1)

        d1_delta =  d1_time - d2_time
        d2_delta = -1 * d1_delta

        drivers[driver1['Abbreviation']]['results'].append(d1_time)
        drivers[driver2['Abbreviation']]['results'].append(d2_time)

        drivers[driver1['Abbreviation']]['delta'].append(d1_delta)
        drivers[driver2['Abbreviation']]['delta'].append(d2_delta)

    elif pd.notna(driver1.Q2) and pd.notna(driver2.Q2):
        d1_time = driver1.Q2/td(seconds=1)
        d2_time = driver2.Q2/td(seconds=1)

        d1_delta =  d1_time - d2_time
        d2_delta = -1 * d1_delta

        drivers[driver1['Abbreviation']]['results'].append(d1_time)
        drivers[driver2['Abbreviation']]['results'].append(d2_time)

        drivers[driver1['Abbreviation']]['delta'].append(d1_delta)
        drivers[driver2['Abbreviation']]['delta'].append(d2_delta)
        
    elif pd.notna(driver1.Q1) and pd.notna(driver2.Q1):
        d1_time = driver1.Q1/td(seconds=1)
        d2_time = driver2.Q1/td(seconds=1)

        d1_delta =  d1_time - d2_time
        d2_delta = -1 * d1_delta

        drivers[driver1['Abbreviation']]['results'].append(d1_time)
        drivers[driver2['Abbreviation']]['results'].append(d2_time)
        
        drivers[driver1['Abbreviation']]['delta'].append(d1_delta)
        drivers[driver2['Abbreviation']]['delta'].append(d2_delta)







# A place to save the results, This can just sit at the end.
try:
    with open('./drivers.json', 'w', encoding='utf-8') as f:
        json.dump(drivers, f, indent=4) # Using indent for human-readable formatting
    print(f"Data successfully dumped to {'drivers.json'}")
except IOError as e:
    print(f"Error writing to file: {e}") 



