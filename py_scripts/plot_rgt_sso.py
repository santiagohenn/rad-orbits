import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the metrics CSV
metrics_file = "./outputs/metrics_summary_ssrgt_1030_AP8.csv"
data = pd.read_csv(metrics_file)

# Create a 3D scatter plot
fig = plt.figure()

color_palette = sns.color_palette("rocket")

# data = pd.DataFrame.filter(lambda entry: entry["height"] < (6371 + 1200), data)

ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(
    data["ND"], 
    data["height"], 
    data["inc"], 
    c=data["percentage_of_access"]*100.0,
    cmap="jet",
    marker='o', 
    s=6
)

# Reverse the x-axis direction
ax.invert_xaxis()

# Set axis labels
ax.set_xlabel('ND')
ax.set_ylabel('Orbit height [km]')
ax.set_zlabel('inclination [°]')

# Title
ax.set_title('SSO w/ RGT')

plt.tight_layout()

# Add a colorbar

colorbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=10)
colorbar.set_label("Perc. of Access")  # Label for the colorbar

# Show the plot
plt.show()