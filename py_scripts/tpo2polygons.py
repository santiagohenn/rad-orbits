import csv
import numpy as np
import pandas as pd
from shapely.geometry import Polygon, mapping
import matplotlib.pyplot as plt
import geojson
from scipy.interpolate import griddata
from shapely.geometry import Polygon, mapping
import matplotlib.colors as mcolors

def read_spenvis_file(file_path, start_line, end_line, start_col, end_col):
    """
    Reads a CSV file between the start_line and end_line (inclusive)
    and returns a list of rows.

    :param file_path: Path to the CSV file
    :param start_line: The starting line (1-indexed) to begin reading
    :param end_line: The ending line (1-indexed) to stop reading
    :return: List of rows between start_line and end_line
    """
    rows = []
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        for current_line, row in enumerate(csv_reader, start=1):
            if current_line >= start_line:
                rows.append(row[start_col:end_col]) # Extract needed columns
            if current_line >= end_line:
                break
    return rows

def save_dataset_csv(file_path, rows):
    """
    Saves the spenvis dataset as the CSV file format that we use.

    :param file_path: Path to the output CSV file
    :param rows: List of rows to write to the CSV file
    """
    with open(file_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)

# Change the model's height here:
model_height_km = 750
data_set_file_folder = './datasets/spenvis'

# Dataset file path
data_set_file_path = f"{data_set_file_folder}/spenvis_tpo_{model_height_km}km.txt"
data_set_grid_path = f"{data_set_file_folder}/grid_spenvis_tpo_{model_height_km}km.txt"

print("Transforming spenvis data to CSV dataset")

# Load grid and particle datasets obtained from spenvis
grid_dataset = read_spenvis_file(data_set_grid_path,27,10916,1,3)
particles_dataset = read_spenvis_file(data_set_file_path,31,10920,0,3)

# Join grid and particles datasets:
for row_idx, row in enumerate(grid_dataset):
    for particle_metric in particles_dataset[row_idx]:
        row.append(particle_metric)

# Add headers
grid_dataset.insert(0, ["lat","lon","B_Gauss","L_8R_3_dE_n","Flux_cm_u-2_s_u-1_50MeV"])

# Save dataset in the format we like
data_set_file_path = data_set_file_path[:-4] + ".csv"
save_dataset_csv(data_set_file_path, grid_dataset)

# Load mf data
data = pd.read_csv(data_set_file_path)
latitudes = data['lat'].values
longitudes = data['lon'].values
values = data['Flux_cm_u-2_s_u-1_50MeV'].values

# Define grid size and create grid points
num_bins = 120
lon_grid = np.linspace(min(longitudes), max(longitudes), num_bins)
lat_grid = np.linspace(min(latitudes), max(latitudes), num_bins)
grid_lon, grid_lat = np.meshgrid(lon_grid, lat_grid)

print("I'm working ... this takes a while. Be patient.")

# Interpolate the data to create a grid
grid_values = griddata((longitudes, latitudes), values, (grid_lon, grid_lat), method='linear')

# Create contour lines based on interpolated grid
contour_set = plt.contour(grid_lon, grid_lat, grid_values, levels = np.logspace(1, 6, 6))

# Extract contours as polygons
polygons = []
for i, collection in enumerate(contour_set.collections):
    level = contour_set.levels[i]  # Get contour level
    for path in collection.get_paths():
        # Convert the path to a polygon if it's closed
        if path.vertices.shape[0] > 2:  # Must have at least 3 points to form a polygon
            poly = Polygon(path.vertices)
            polygons.append({"geometry": mapping(poly), "level": level})

print("Writing polygon files.")

with open(f'outputs/polygons_tpo_{model_height_km}.json', 'w') as f:
    geojson.dump(polygons, f)

print("Done!.")