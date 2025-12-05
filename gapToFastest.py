import fastf1
import matplotlib.pyplot as plt
from timple.timedelta import strftimedelta
import pandas as pd
import fastf1.plotting
from fastf1.core import Laps

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None)

year = 2022
# Errors when the round changes on Line 24, check LAPS()
round = 2

session = fastf1.get_session(year, round, 'Q')
session.load()

drivers = pd.unique(session.laps['Driver'])

list_fastest_laps = list()

for driver in drivers:
    driver_fastest_lap = session.laps.pick_drivers(driver).pick_fastest()
    if driver_fastest_lap is not None and not driver_fastest_lap.empty:
        list_fastest_laps.append(driver_fastest_lap)
fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
pole_lap = fastest_laps.pick_fastest()
fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

team_colors = list()
for index, lap, in fastest_laps.iterlaps():
    color = fastf1.plotting.get_team_color(lap['Team'], session=session)
    team_colors.append(color)

fig, ax = plt.subplots()
ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'], color=team_colors, edgecolor = 'grey')
ax.set_yticks(fastest_laps.index)
ax.set_yticklabels(fastest_laps['Driver'])

ax.invert_yaxis()
ax.set_axisbelow(True)
ax.xaxis.grid(True, which='major', linestyle = '--', color = 'black', zorder = -1000)

lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')
plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")
plt.show()