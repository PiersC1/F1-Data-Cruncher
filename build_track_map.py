import fastf1
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from matplotlib.collections import LineCollection


session = fastf1.get_session(2026, 1, 'Q')
session.load(telemetry=True)

laps = session.laps
lap = laps.pick_fastest()

telemetry = lap.get_telemetry()

x = telemetry['X'].values
y = telemetry['Y'].values
speed = telemetry['Speed'].values

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
norm = plt.Normalize(speed.min(), speed.max())
cmap = cm.RdYlGn

lc = LineCollection(segments, cmap = cmap, norm = norm, linewidth = 3)
lc.set_array(speed[:-1])

fig, ax = plt.subplots(figsize = (10, 8))
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

ax.add_collection(lc)
ax.autoscale()
ax.set_aspect('equal')
ax.axis('off')

cbar = fig.colorbar(lc, ax=ax, fraction=0.02, pad=0.02)
cbar.set_label('Speed (km/h)', color='white')
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')

plt.title(f"Speed Map — {lap['Driver']} | {session.event['EventName']} {session.event.year}",  color='white', fontsize=14)
plt.tight_layout()
plt.show()
