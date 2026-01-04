import pandas as pd
import fastf1
from fastf1.core import Laps
import statistics
import matplotlib.pyplot as plt
from datetime import timedelta



def load_data(year):
    eventSchedule = fastf1.get_event_schedule(year)
    events = pd.DataFrame(eventSchedule)
    return events


def parse_data(events, session_type, percent_or_raw, year):
    drivers_gap = {}
    for _, row in events.iterrows():
        if row['RoundNumber'] == 0:
            continue # Filter out testing sessions
        event_name = row['Country']

        session = fastf1.get_session(year, event_name, session_type)
        session.load()

        drivers = pd.unique(session.laps['Driver'])
        keys = drivers_gap.keys()
        for driver in drivers:
            if driver not in keys:
                drivers_gap[driver] = []


        list_fastest_laps = list()

        for driver in drivers:
            driver_fastest_lap = session.laps.pick_drivers(driver).pick_fastest()
            if driver_fastest_lap is not None and not driver_fastest_lap.empty:
                list_fastest_laps.append(driver_fastest_lap)
        fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
        pole_lap = fastest_laps.pick_fastest()
        if percent_or_raw == 1:
            fastest_laps['LapTimePercent'] = ((fastest_laps['LapTime'] - pole_lap['LapTime'])/pole_lap['LapTime']) * 100
        else:
            fastest_laps['RawGap'] = (fastest_laps['LapTime'] - pole_lap['LapTime'])/timedelta(seconds=1) # Raw Gap to pole instead of percentage
        fastest_laps = pd.DataFrame(fastest_laps)
        
        if percent_or_raw == 1:
            for _, row in fastest_laps.iterrows():
                drivers_gap[f'{row['Driver']}'].append(row['LapTimePercent'])
        else:
            for _, row in fastest_laps.iterrows():
                drivers_gap[f'{row['Driver']}'].append(row['RawGap'])
    return drivers_gap




def calculate_average(drivers_gap):
    driver_average_time = {}
    for driver in drivers_gap:
        driver_average_time[driver] = statistics.mean(drivers_gap[driver])
    # Sort the dictionary using the values so that it is actually useful
    driver_average_time = dict(sorted(driver_average_time.items(), key=lambda item: item[1]))
    return driver_average_time
    


def visualise(driver_average_time):
    x_vals = driver_average_time.keys()
    y_vals = driver_average_time.values()

    plt.bar(x_vals, y_vals)

    plt.xlabel = "Driver"
    plt.ylabel = "Gap to Pole"
    plt.title = "Drivers Gap to Pole Over a Season"

    plt.show()

def main():
    year = int(input("What year would you like to analyze? (2025 is chached) "))
    event_schedule_for_year = load_data(year)
    session_type = input("What session should be analyzed? 'Q' for Quali (Reccomended), 'R' for race, 'P 1/2/3' for practice ")
    raw_or_percent = input("Do you want the gap to pole as raw seconds or as a percent? ")
    if "per" in raw_or_percent or '%' in raw_or_percent:
        raw_or_percent = 1 
    else:
        raw_or_percent = 0
    drivers_with_gap_at_every_round = parse_data(event_schedule_for_year, session_type, raw_or_percent, year)
    driver_average_time_dict = calculate_average(drivers_with_gap_at_every_round)
    visualise(driver_average_time_dict)


if __name__ == '__main__':
    main()