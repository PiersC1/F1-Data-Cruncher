import json
import matplotlib.pyplot as plt

drivers = {}
team_color = {'McLaren' : '#F98E1D', 'Mercedes' : '#72EFD9', 'Red Bull Racing' : '#121f45', 'Racing Bulls' : "#1d516c", 'Williams' : '#00A0DD', 'Ferrari' : '#DD0000', 'Alpine' : "#D52EB9", 'Aston Martin' : "#1F741F", 'Kick Sauber' : '#00FF00', 'Haas F1 Team' : "#000000"}
driver_teams = {}
name_abbrev = {}
driver_rating = {}
driver_to_team = {}

DEFAULT_RATING = 90
DELTA_MULTIPLIER = 5
CAR_PERFORMANCE_BIAS = 4 # Higher numbers reduce bias

try:
    with open('./drivers.json', 'r', encoding='utf-8') as f:
        drivers = json.load(f)
except IOError as e:
    print(f"Error reading from file: {e}") 

try:
    with open('./name_abbrev.json', 'r', encoding='utf-8') as f:
        name_abbrev = json.load(f)
except IOError as e:
    print(f"Error reading from file: {e}")

try:
    with open('./driver_teams.json', 'r', encoding='utf-8') as f:
        driver_teams = json.load(f)
except IOError as e:
    print(f"Error reading from file: {e}")



for team in driver_teams:
    d1_name = driver_teams[team][0]
    d2_name = driver_teams[team][1]

    driver_to_team[name_abbrev[d1_name]] = team
    driver_to_team[name_abbrev[d2_name]] = team

    d1_deltas = drivers[name_abbrev[d1_name]]['delta']
    d2_deltas = drivers[name_abbrev[d2_name]]['delta']

    d1_qualis = drivers[name_abbrev[d1_name]]['pos']
    d2_qualis = drivers[name_abbrev[d2_name]]['pos']

    d1_avg = sum(d1_qualis)/len(d1_qualis)
    d2_avg = sum(d2_qualis)/len(d2_qualis)

    d1_delta = sum(d1_deltas)/len(d1_deltas)
    d2_delta = sum(d2_deltas)/len(d2_deltas)

    driver_rating[d1_name] = round(DEFAULT_RATING + (-d1_delta * DELTA_MULTIPLIER) + (20 - d1_avg)/CAR_PERFORMANCE_BIAS, 2)
    driver_rating[d2_name] = round(DEFAULT_RATING + (-d2_delta * DELTA_MULTIPLIER) + (20 - d2_avg)/CAR_PERFORMANCE_BIAS, 2)
    

sorted_drivers = sorted(driver_rating.items(), key=lambda x: x[1], reverse=True)
#print(sorted_drivers)

for i in range(len(sorted_drivers)):
    curr_driver = sorted_drivers[i]
    plt.bar(name_abbrev[curr_driver[0]], curr_driver[1], color=team_color[driver_to_team[name_abbrev[curr_driver[0]]]])

plt.show()

try:
    with open('./quali_ratings.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_drivers, f, indent=4) # Using indent for human-readable formatting
    print(f"Data successfully dumped to {'name_abbrev.json'}")
except IOError as e:
    print(f"Error writing to file: {e}") 