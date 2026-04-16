import fastf1
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from matplotlib.collections import LineCollection


session = fastf1.get_session(2026, 3, 'R')
session.load(telemetry=True)

laps = session.laps
lap = laps.pick_drivers(['PIA']).pick_accurate().pick_lap(2)

telemetry = lap.get_telemetry()

braking = telemetry['Brake'].values

x = telemetry['X'].values
y = telemetry['Y'].values
m = []
for i in range(1, len(x)):
    m.append((y[i]-y[i-1])/(x[i]-x[i-1]))
    if i == 1:
        m.insert(0, m[0])

speed = telemetry['Speed'].values

throttle = telemetry['Throttle'].values

corner = []
for i in range(1, len(speed)):
    if(abs(m[i] - m[i-1]) > 0.03):
        corner.append(1)
    else:
        corner.append(0)
    if i == 1:
        corner.insert(0, corner[0])
corner = np.array(corner)

# Need to get to accel b/c no data for that
time_seconds = telemetry['Time'].dt.total_seconds().values
speed_ms = speed * (1000 / 3600)  # km/h to m/s

# Still some random Accel spikes
# Long accel
accel = np.diff(speed_ms) / np.diff(time_seconds) / 9.81  # in G

'''
accel = []
for i in range(1, len(speed)):
    accel.append(((speed[i] - speed[i-1]) * (1000/3600))/dt.timedelta(time[i]-time[i-1]).total_seconds())/9.81
    if i == 1:
        accel.insert(0, accel[0])
accel = np.array(accel)
'''

superClipping = []
for i in range(0, len(accel)):
    # Exclude coasting corners 
    if accel[i] < 0 and not braking[i] and throttle[i] > 98:
        superClipping.append(1)
    else:
        superClipping.append(0)
superClipping = np.array(superClipping)


points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

metrics = {
    'Speed (km/h)': speed,
    'Throttle (%)': throttle,
    'Superclipping': superClipping,
    'Long Accel [G]': accel,
    'Corner': corner,
    #'m':np.array(m)
}

for label, data in metrics.items():
    norm = plt.Normalize(data.min(), data.max())
    cmap = cm.RdYlGn

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    lc = LineCollection(segments, cmap=cmap, norm=norm, linewidth=2)
    lc.set_array(data[:-1])

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.add_collection(lc)
    ax.autoscale()
    ax.set_aspect('equal')
    ax.axis('off')

    cbar = fig.colorbar(lc, ax=ax, fraction=0.02, pad=0.02)
    cbar.set_label(label, color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')

    ax.set_title(label, color='white', fontsize=12)
    plt.tight_layout()
plt.show()