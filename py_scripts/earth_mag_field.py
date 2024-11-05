import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np

# Empty figure with axis
fig = plt.figure(figsize=(10, 6))

# Load the data from CSV
data = pd.read_csv('C:/Projects/rad-orbits/datasets/F_map_mf_2020/F_Grid_2020.csv')  # Replace 'data.csv' with your file path

# Extract latitude, longitude, and mag field values
latitudes = data['lat'].values
longitudes = data['lon'].values
values = data['mag_field'].values

# World plot
ax = fig.add_subplot()

sc = ax.scatter(longitudes, latitudes, c=values, cmap='inferno', s=10, alpha=0.6)
plt.colorbar(sc, label='nT', shrink=0.6)

# Low res world map case7\coverage-aware\ne_polygons_73d575dcc86cf4911d290f7444b308be57c90c8534b86d8eeb86239284f6f043_1.json
world = gpd.read_file("C:/Projects/rad-orbits/datasets/countries/ne_110m_admin_0_countries.shp")

# Basic worldmap
world.plot(
    ax=ax,
    color="lightgray",
    edgecolor="black",
    alpha=0.5,
    legend=True
)

# Show the plot
plt.xlabel('Longitude [Degrees]')
plt.ylabel('Latitude [Degrees]')
plt.tight_layout()
plt.title('Earth Magnetic Field [nT]')
plt.show()
