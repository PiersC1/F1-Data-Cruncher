import pandas as pd
import fastf1



year = 2025

eventSchedule = fastf1.get_event_schedule(year)
events = pd.DataFrame(eventSchedule)



roundNumLookUp = {}

for i in range(events['RoundNumber'].count()):
    if events['RoundNumber'][i] != 0:
        roundNumLookUp[events['Country'][i]] = events['RoundNumber'][i]

print(roundNumLookUp)

