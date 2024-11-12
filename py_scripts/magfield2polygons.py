import numpy as np
import pandas as pd
from shapely.geometry import Polygon, mapping
import matplotlib.pyplot as plt
import geojson
from scipy.interpolate import griddata
from shapely.geometry import Polygon, mapping

# Load mf data
data = pd.read_csv('./datasets/F_map_mf_2020/F_Grid_2020.csv')
latitudes = data['lat'].values
longitudes = data['lon'].values
values = data['mag_field'].values

# Define grid size and create grid points
num_bins = 120
lon_grid = np.linspace(min(longitudes), max(longitudes), num_bins)
lat_grid = np.linspace(min(latitudes), max(latitudes), num_bins)
grid_lon, grid_lat = np.meshgrid(lon_grid, lat_grid)

# Interpolate the data to create a grid
grid_values = griddata((longitudes, latitudes), values, (grid_lon, grid_lat), method='cubic')

# Create contour lines based on interpolated grid
contour_set = plt.contour(grid_lon, grid_lat, grid_values, levels=10)

# Extract contours as polygons
polygons = []
for i, collection in enumerate(contour_set.collections):
    level = contour_set.levels[i]  # Get contour level
    for path in collection.get_paths():
        # Convert the path to a polygon if it's closed
        if path.vertices.shape[0] > 2:  # Must have at least 3 points to form a polygon
            poly = Polygon(path.vertices)
            polygons.append({"geometry": mapping(poly), "level": level})

with open('outputs/polygons.json', 'w') as f:
    geojson.dump(polygons, f)