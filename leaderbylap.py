import fastf1
import pandas as pd
import math
import matplotlib.pyplot as plt




def pretty_print(dr):
    for d in dr:
        print(f"Driver: {number_name[d]} Points: {dr[d]}")
    x_vals = dr.keys()
    y_vals = dr.values()
    plt.bar(x_vals, y_vals)
    plt.xlabel("Drivers")
    plt.ylabel("Points")
    plt.title("If points were awarded every lap")
    plt.show()

year = 2025
points_by_pos = {
    1 : 25,
    2 : 18,
    3 : 15,
    4 : 12,
    5 : 10,
    6 : 8,
    7 : 5,
    8 : 4,
    9 : 2,
    10 : 1,
    11 : 0,
    12 : 0,
    13 : 0,
    14 : 0,
    15 : 0,
    16 : 0,
    17 : 0,
    18 : 0,
    19 : 0,
    20 : 0
}

number_name = {}
drivers = {} # 'driverName' : points (int)

eventSchedule = fastf1.get_event_schedule(year)

events = pd.DataFrame(eventSchedule)

for _, row in events.iterrows():
    if row['RoundNumber'] == 0:
        continue # Filter out testing sessions
    event = eventSchedule.get_event_by_round(row['RoundNumber'])
    race = event.get_race()
    race.load()
    # Updating Driver Roster
    keys = drivers.keys()
    for driver in race.drivers:
        if driver not in keys:
            drivers[driver] = 0
    keys = drivers.keys()
    laps = race.laps
    for driver in keys:
        driver_laps = laps.pick_drivers(driver)
        for _, lap in driver_laps.iterlaps():
            if driver not in number_name.keys():
                number_name[driver] = lap['Driver']
            if not math.isnan(lap['Position']):
                drivers[driver] += points_by_pos[int(lap['Position'])]

sorted_drivers = dict(sorted(drivers.items(), key=lambda item: item[1], reverse=True))



pretty_print(sorted_drivers)
