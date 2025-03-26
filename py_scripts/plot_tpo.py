import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import json
from shapely.geometry import shape
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from descartes import PolygonPatch
import seaborn as sns
import matplotlib.colors as mcolors

model_height_km = 350
plot_polygons = False

dataset_file_path = f'./datasets/spenvis/spenvis_tpo_{model_height_km}km.csv'

color_palette = sns.color_palette("rocket")
fig = plt.figure(figsize=(10, 6))

# Load the data from CSV, here I took the data from spenvis
data = pd.read_csv(dataset_file_path)

# Extract latitude, longitude, and mag field values
latitudes = data['lat'].values
longitudes = data['lon'].values
# values = data['B_Gauss'].values
values = data['Flux_cm_u-2_s_u-1_50MeV'].values

color_norm = mcolors.LogNorm(vmin=1, vmax=1e4)

# World plot
ax = fig.add_subplot()
sc = ax.scatter(longitudes, latitudes, c=values, cmap='jet', s=15, alpha=0.6, marker="s", norm=color_norm)
plt.colorbar(sc, label=r'$\text{AP-8 MAX Flux } \, in \, \text{MeV (cm}^{-2} \, \text{s}^{-1})$', shrink=0.6)
world = gpd.read_file("./datasets/countries/ne_110m_admin_0_countries.shp")
world.plot(
    ax=ax,
    color="lightgray",
    edgecolor="black",
    alpha=0.5,
    legend=True
)

if plot_polygons:

    # Load the JSON file containing the polygons
    with open(f'outputs/polygons_tpo_{model_height_km}.json', 'r') as f:
        polygons = json.load(f)

    # Modify this list based on the levels you want to plot
    levels_to_plot = [10.0, 100.0, 1000.0]  

    # Filter and plot polygons
    color_counter = 0
    for polygon_data in polygons:
        level = polygon_data.get("level")
        if level in levels_to_plot:
            try:
                # Extract the coordinates of the polygon
                coordinates = polygon_data['geometry']['coordinates'][0]  # Use only the exterior ring

                # Create a Polygon patch with no fill
                outline_patch = mpatches.Polygon(coordinates, closed=True, edgecolor='black', fill=False, linewidth=1.5)
                ax.add_patch(outline_patch)
                color_counter = color_counter + 1

            except (IndexError, TypeError, KeyError) as e:
                print(f"Skipping a polygon due to error: {e}")

# Show the plot
plt.xlabel('Longitude [Degrees]')
plt.ylabel('Latitude [Degrees]')
plt.tight_layout()
plt.title(f'Trapped protons according to the AP-8 model, at {model_height_km}Km of height')
plt.savefig(f'outputs/img/trapped_protons_{model_height_km}.png', format='png', bbox_inches='tight')
plt.savefig(f'outputs/img/trapped_protons_{model_height_km}.pdf', format='pdf', bbox_inches='tight')
plt.show()
