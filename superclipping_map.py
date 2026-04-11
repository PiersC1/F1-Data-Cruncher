import fastf1
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from matplotlib.collections import LineCollection


'''
How will we know superclipping?
if accel is negative and brake is false
'''

session = fastf1.get_session(2026, 2, 'Q')
session.load(telemetry=True)

laps = session.laps
lap = laps.pick_fastest()

telemetry = lap.get_telemetry()

braking = telemetry['Brake'].values

x = telemetry['X'].values
print(type(x))
y = telemetry['Y'].values
speed = telemetry['Speed'].values
# Need to get to accel b/c no data for that
accel = []
for i in range(1, len(speed)):
    accel.append(speed[i] - speed[i-1])
    if i == 1:
        accel.insert(0, accel[0])
accel = np.array(accel)

superClipping = []
for i in range(0, len(accel)):
    # Figure out a way to exclude corners
    if accel[i] < 0 and not braking[i]:
        superClipping.append(1)
    else:
        superClipping.append(0)
superClipping = np.array(superClipping)


points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
norm = plt.Normalize(superClipping.min(), superClipping.max())
cmap = cm.RdYlGn

lc = LineCollection(segments, cmap = cmap, norm = norm, linewidth = 3)
lc.set_array(superClipping[:-1])

fig, ax = plt.subplots(figsize = (10, 8))
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

ax.add_collection(lc)
ax.autoscale()
ax.set_aspect('equal')
ax.axis('off')

cbar = fig.colorbar(lc, ax=ax, fraction=0.02, pad=0.02)
cbar.set_label('Accel (delta km/h)', color='white')
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')

plt.title(f"Accel Map — {lap['Driver']} | {session.event['EventName']} {session.event.year}",  color='white', fontsize=14)
plt.tight_layout()
plt.show()
