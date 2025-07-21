
import pandas as pd
from matplotlib.lines import Line2D
from cartopy import crs as ccrs, feature as cfeature
import polyline
import ffmpeg
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import datetime
import matplotlib.animation as animation
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from celluloid import Camera

camino = pd.read_csv("../Data/Processed_data/camino.csv")
print(camino.columns)

camino = camino[~camino['name'].str.contains('Monparnasse', case=False, na=False)]

# Sort the data frame in date order
camino.sort_values(by='start_date_local_dt', ascending = True, inplace = True)

# Processing the data
camino_id_list = camino.id.unique()

# Create a look up dictionary for each id with day number, distance that day, names of where I walked from / to
info_lookup = {}
for id in camino_id_list:

    info_lookup[id] = {}
    info_lookup[id]['title'] = camino[camino['id'] == id]['name'].iloc[0]
    info_lookup[id]['elevation'] = camino[camino['id'] == id]['total_elevation_gain'].iloc[0]
    info_lookup[id]['distance'] = camino[camino['id'] == id]['distance'].iloc[0]

def return_lat_long(coords):

    """
    Take a polyline code, decode it into a list of latitude and longitude coordinates
    """

    # TODO turn it into a dictionary of lists so we can add in total distance and day

    data = {}

    coordinates = polyline.decode(coords)

    latitudes = [coordinate[0] for coordinate in coordinates]
    longitudes = [coordinate[1] for coordinate in coordinates]

    return latitudes, longitudes

data = {}
data['all_camino_longs'] = []
data['all_camino_lats'] = []
data['id'] = []

for id in camino_id_list:

    print(id)

    coords = camino[camino['id'] == id]['map.summary_polyline'].iloc[0]

    lat, long = return_lat_long(coords)

    print([id] * len(long))

    data['all_camino_longs'].extend(long)
    data['all_camino_lats'].extend(lat)
    data['id'].extend([id] * len(long))

print(len(data['all_camino_lats']))
print(len(data['all_camino_longs']))
print(len(data['id']))

########################################################################################################################
# Geeks for geeks tutorial
# https://www.geeksforgeeks.org/python/matplotlib-animate-multiple-lines/


########################################################################################################################
import pandas as pd
import polyline
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import datetime
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Lets try and bring the maps in to this
projPC = ccrs.PlateCarree()
latN = 44
latS = 41.5
lonW = -10
lonE = 0
cLat = (latN + latS) / 2
cLon = (lonW + lonE) / 2
res = '50m'

fig = plt.figure(figsize=(11, 5))
ax = plt.subplot(1, 1, 1, projection=projPC)
ax.set_title('Plate Carree')
gl = ax.gridlines(
    draw_labels=True, linewidth=0.5, color='white', alpha=0.5, linestyle='--'
)
ax.set_extent([lonW, lonE, latS, latN], crs=projPC)
ax.add_feature(cfeature.LAKES)
ax.add_feature(cfeature.RIVERS)
ax.add_feature(cfeature.LAND, alpha=0.9)
ax.add_feature(cfeature.OCEAN, alpha=0.6)
ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='grey')

# counter = 0
# for id in camino_id_list:
#
#     coords = camino[camino['id'] == id]['map.summary_polyline'].iloc[0]
#
#     long, lat = return_lat_long(coords)
#
#     if counter % 2 == 0:
#         col_to_plot = "coral"
#     else:
#         col_to_plot = "red"  # deeppink
#
#     plt.plot(long, lat, 'r-', alpha=1, color=col_to_plot)
#
#     counter += 1

xdata, ydata = [], []

line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    # t is a parameter which varies
    # with the frame number
    t = i # 0.1 * i # 100 + i

    # x, y values to be plotted
    # x = sampled_longs[t] # t * np.sin(t)
    # y = sampled_lats[t] # t * np.cos(t)
    x = data['all_camino_longs'][t:t+1]
    y = data['all_camino_lats'][t:t+1]
    id = data['id'][t:t+1][0]

    # appending values to the previously
    # empty x and y data holders
    xdata.extend(x)
    ydata.extend(y)
    line.set_data(xdata, ydata)

    # Info to upload
    title = info_lookup[id]['title']
    elev = info_lookup[id]['elevation']
    dist = info_lookup[id]['distance']

    # Remove old legend and add a new one
    # line.set_label()
    # line.set_label(f'{title}')
    legend_handle = Line2D([0], [0], color='none', label=f'{title} \n Dist: {round(dist/100)}km \n Elev: {round(elev)}m')
    ax.legend(handles=[legend_handle], bbox_to_anchor=(0.4, -0.07))

    return line,

# calling the animation function
# anim = animation.FuncAnimation(fig, animate, init_func=init,
#                                frames=200, interval=0.01, blit=True)
frames = range(0, len(data['all_camino_lats']), 30)
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=frames, interval=20, blit=False)

# anim.save(filename="test.gif", fps=30, writer="pillow")

plt.show()

#anim.save('growingCoil.gif', fps=30, writer="pillow")  # writer='ffmpeg'



# TODO remove the weird final point that is skewing the data back to the beginning

# TODO add total distance and elevation as inserts that go up