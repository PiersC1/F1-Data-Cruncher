import pandas as pd
import fastf1
from fastf1.core import Laps
import statistics
import matplotlib.pyplot as plt
from datetime import timedelta


year = 2025

eventSchedule = fastf1.get_event_schedule(year)
events = pd.DataFrame(eventSchedule)

drivers_gap = {}
# Format: 'Name' : [GapR1, GapR2, ...]

# print(roundNumLookUp)

# Get quali gap by round

# Every round: 
#           1. Check if there is a new driver DONE
#               1a. If new, add to the dictionary DONE
#           2. Update Gap to P1 as a percentage of the Pole Laptime
for i in range(events['RoundNumber'].count()):
    round = -1
    if events['RoundNumber'][i] != 0:
        round = events['Country'][i]
    else:
        continue

    session = fastf1.get_session(2025, round, 'Q')
    session.load()

    drivers = pd.unique(session.laps['Driver'])
    keys = drivers_gap.keys()
    for driver in drivers:
        if driver not in keys:
            drivers_gap[f'{driver}'] = []


    list_fastest_laps = list()

    for driver in drivers:
        driver_fastest_lap = session.laps.pick_drivers(driver).pick_fastest()
        if driver_fastest_lap is not None and not driver_fastest_lap.empty:
            list_fastest_laps.append(driver_fastest_lap)
    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
    pole_lap = fastest_laps.pick_fastest()
    #fastest_laps['LapTimePercent'] = ((fastest_laps['LapTime'] - pole_lap['LapTime'])/pole_lap['LapTime']) * 100
    fastest_laps['LapTimePercent'] = (fastest_laps['LapTime'] - pole_lap['LapTime'])/timedelta(seconds=1) # Raw Gap to pole instead of percentage
    fastest_laps = pd.DataFrame(fastest_laps)
    
    for _, row in fastest_laps.iterrows():
        drivers_gap[f'{row['Driver']}'].append(row['LapTimePercent'])





# TODO: Update gap to P1 as apercentage of the pole lap
# Qestions: How to do this with different sessions having different drivers and different conditions?
# Base Formula = (Drivers best time - Pole time)/Pole time
# Maybe go through Q1 and update the drivers gap to P1 there, 
# then repeat for Q2 and Q3 incrementing the number of sessions that the driver has taken place in?


DriverToAverage = {}
for driver in drivers_gap:
    DriverToAverage[f'{driver}'] = statistics.mean(drivers_gap[f'{driver}'])
DriverToAverage = dict(sorted(DriverToAverage.items(), key=lambda item: item[1]))
    
x_vals = DriverToAverage.keys()
y_vals = DriverToAverage.values()


plt.bar(x_vals, y_vals)
plt.show()


print(DriverToAverage)