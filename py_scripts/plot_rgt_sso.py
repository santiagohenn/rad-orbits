import pandas as pd
import matplotlib.pyplot as plt

# Load the metrics CSV
metrics_file = "./outputs/metrics_ssrgt.csv"
data = pd.read_csv(metrics_file)

# Create a 3D scatter plot
fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(
    data["ND"], 
    data["height"], 
    data["inc"], 
    c=data["metric"],
    cmap='rocket',
    marker='o', 
    s=2
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

