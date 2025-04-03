import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

folder = "ssrgt_1030_AP8_RAAN"

# Load the metrics CSV
metrics_file = f"./outputs/metrics_summary_{folder}csv"
data = pd.read_csv(metrics_file)

data = data[data.height < 800]

fig1 = plt.figure()
ax = fig1.add_subplot(111)
scatter = ax.scatter(
    data["ND"], 
    data["height"],
    c=data["fluence"] * 1000.0,
    cmap="viridis", 
    norm=mcolors.LogNorm(vmin=1E7, vmax=4E7),
    #vmin=1E9, 
    #vmax=1E8,
    marker='o', 
    s=40
)

colorbar = fig1.colorbar(scatter, ax=ax, shrink=0.5, aspect=10, pad=0.1)
colorbar.set_label("Fluencia [protones/cm-2]")


# Reverse the x-axis direction
# ax.invert_xaxis()

# Set axis labels
ax.grid(True, axis='x', linestyle='--', linewidth=0.7, color='gray', alpha=0.7)
ax.set_axisbelow(True)
ax.set_xticks(range(1,21,1))
ax.set_xlabel('ND (días para repetición)')
ax.set_ylabel('Altura orbital [km]')
# ax.set_zlabel('inclinación [°]')


plt.tight_layout()
plt.show()

# Create a 3D scatter plot
# fig = plt.figure()

# color_palette = sns.color_palette("rocket")
