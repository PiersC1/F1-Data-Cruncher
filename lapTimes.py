import seaborn as sns
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1')

raceNum = 8
year = 2024

races = fastf1.get_event_schedule(year)
event = races.get_event_by_round(raceNum)
race = event.get_race()
race.load()
driver = 'VER'
driver_laps = race.laps.pick_drivers(driver).pick_quicklaps().reset_index()

fig, ax = plt.subplots(figsize=(8,8))

sns.scatterplot(data = driver_laps,
                x="LapNumber",
                y="LapTime",
                ax=ax,
                hue="Compound",
                palette=fastf1.plotting.get_compound_mapping(session = race),
                s=80,
                linewidth=0,
                legend='auto')

ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time")

ax.invert_yaxis()
plt.suptitle(f"{driver} laptimes from {race}")

plt.grid(color='w', which='major', axis='both')
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.show()
