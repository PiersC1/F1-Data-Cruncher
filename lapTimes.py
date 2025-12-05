import seaborn as sns
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1')

raceNum = 24
year = 2025

races = fastf1.get_event_schedule(year)
event = races.get_event_by_round(raceNum)
race = event.get_session(2)
race.load()
drivers = ['NOR', 'VER', 'PIA']

driver_laps = race.laps.pick_drivers(drivers).pick_quicklaps(threshold=1.20).reset_index() 

#.pick_quicklaps() go between pick_drivers() and reset_index() when analysing not practice

fig, ax = plt.subplots(figsize=(8,8))

sns.scatterplot(data = driver_laps,
                x="LapNumber",
                y="LapTime",
                ax=ax,
                hue="Compound",
                style=driver_laps['Driver'],
                palette=fastf1.plotting.get_compound_mapping(session = race),
                s=80,
                linewidth=0,
                legend='auto')

ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time")

ax.invert_yaxis()
plt.suptitle(f" laptimes from {race}")

plt.grid(color='w', which='major', axis='both')
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()
