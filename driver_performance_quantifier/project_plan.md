# What is the goal?
- Quantify Driver Race Performance
- Quantify Driver Qualifying Performance

# Sub Goals?
- On Race Performance
- - Should it be split into track types? Weather? How should I determine Racecraft?
- On Quali Performance
- - Track type? Consistency at 100%?

# Plan
- Start with qualifying (Easier, less data points, less laps to analyze)
- Don't split based on track type.
- Get teammate delta -> set the mean as 0 -> use that to determine qualifying performance
1. Get teammate delta over the season (NOR -0.1 PIA +0.1 <-- This indicates that NOR was 0.1s faster on average over the season)
2. Because of how deltas work when stored this way the mean will be 0.
3. Pick a default quali performance numer (e.g. 95)
4. Delta/2 + Default + 20-avg quali position/5* (to try and not punish good drivers in good cars)
