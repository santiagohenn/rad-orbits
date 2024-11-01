import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata
import numpy as np

# Load the data from CSV
data = pd.read_csv('C:/Projects/rad-orbits/datasets/F_map_mf_2020/F_Grid_2020.csv')

# Extract latitude, longitude, and values
latitudes = data['lat'].values
longitudes = data['lon'].values
values = data['value'].values

# Create a Basemap instance for the world map
plt.figure(figsize=(12, 6))
m = Basemap(projection='mill', llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180, resolution='c')

# Draw map features
m.drawcoastlines()
m.drawcountries()
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='lightgray', lake_color='aqua')

# Generate a grid to interpolate the values
grid_lon, grid_lat = np.meshgrid(
    np.linspace(-180, 180, 500),
    np.linspace(-90, 90, 250)
)

# Interpolate the values to the grid
grid_values = griddata((longitudes, latitudes), values, (grid_lon, grid_lat), method='linear')

# Convert grid coordinates to map projection
x, y = m(grid_lon, grid_lat)

# Plot the heatmap using pcolormesh
heatmap = m.pcolormesh(x, y, grid_values, shading='auto', cmap='inferno')
plt.colorbar(heatmap, label='nanoTesla')

# Show the plot
plt.title('NanoTesla Heatmap')
plt.show()
