import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import json
from shapely.geometry import shape
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from descartes import PolygonPatch
import matplotlib.patches as mpatches
import seaborn as sns

color_palette = sns.color_palette("rocket")
fig = plt.figure(figsize=(10, 6))

# Load the data from CSV, here I took the latest data from NASA
data = pd.read_csv('./datasets/F_map_mf_2020/F_Grid_2020.csv')

# Extract latitude, longitude, and mag field values
latitudes = data['lat'].values
longitudes = data['lon'].values
values = data['mag_field'].values

# World plot
ax = fig.add_subplot()
sc = ax.scatter(longitudes, latitudes, c=values, cmap='jet', s=10, alpha=0.6)
plt.colorbar(sc, label='nT', shrink=0.6)
world = gpd.read_file("./datasets/countries/ne_110m_admin_0_countries.shp")
world.plot(
    ax=ax,
    color="lightgray",
    edgecolor="black",
    alpha=0.5,
    legend=True
)

# Load the JSON file containing the polygons
with open('outputs/polygons_mf.json', 'r') as f:
    polygons = json.load(f)

# Define the levels you want to plot
levels_to_plot = [25000, 30000]  # Modify this list based on the levels you want to plot

# Filter and plot polygons
color_counter = 0
for polygon_data in polygons:
    level = polygon_data.get("level")
    if level in levels_to_plot:
        try:
            # Extract the coordinates of the polygon
            coordinates = polygon_data['geometry']['coordinates'][0]  # Use only the exterior ring

            # Create a Polygon patch with no fill
            outline_patch = mpatches.Polygon(coordinates, closed=True, edgecolor='white', fill=False, linewidth=1.5)
            ax.add_patch(outline_patch)
            color_counter = color_counter + 1

        except (IndexError, TypeError, KeyError) as e:
            print(f"Skipping a polygon due to error: {e}")

# Show the plot
plt.xlabel('Longitude [Degrees]')
plt.ylabel('Latitude [Degrees]')
plt.tight_layout()
plt.title('Earth Magnetic Field [nT]')
plt.savefig('outputs/saa_overview.pdf', format='pdf', bbox_inches='tight')
plt.show()
