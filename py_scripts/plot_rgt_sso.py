import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

folder = "ssrgt_1030_AP8"

# Load the metrics CSV
metrics_file = f"./outputs/metrics_summary_{folder}.csv"
data = pd.read_csv(metrics_file)

# fig1 = plt.figure()
# ax = fig1.add_subplot(111, projection='3d')
# scatter = ax.scatter(
#     data["ND"], 
#     data["height"], 
#     data["inc"], 
#     marker='o', 
#     s=6
# )

# # Reverse the x-axis direction
# ax.invert_xaxis()

# # Set axis labels
# ax.set_xlabel('ND (días para repetición)')
# ax.set_ylabel('Altura orbital [km]')
# ax.set_zlabel('inclinación [°]')
# plt.tight_layout()
# plt.show()


# Create a 3D scatter plot
fig = plt.figure()

color_palette = sns.color_palette("rocket")

ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(
    data["ND"], 
    data["height"], 
    data["inc"], 
    c=data["fluence"] * 1000.0,
    cmap="viridis", 
    norm=mcolors.LogNorm(vmin=1E7, vmax=1E10),
    #vmin=1E7,
    #vmax=1E10,
    marker='o', 
    alpha=0.9,
    s=8
)

# Reverse the x-axis direction
ax.invert_xaxis()

# Set axis labels
ax.set_xticks(range(1,21,2))
ax.set_xlabel('ND (días para repetición)')
ax.set_ylabel('Altura orbital [km]')
ax.set_zlabel('inclinación [°]')

# Title
# ax.set_title(r"Average time until a $100 \, \frac{MeV}{s \, cm^{2}}$ is encountered, in minutes")
# ax.set_title(r"$\text{Fluencia para energías} > 10.00 \, \text{MeV, protones / cm}^{-2}$" "\n" r"$\text{en órbitas SSRGT}$")

plt.tight_layout()

# Add a colorbar
fig.subplots_adjust(bottom=0.2)
colorbar = fig.colorbar(scatter, ax=ax, orientation='horizontal', fraction=0.05, shrink=0.9, aspect=15, pad=0.13)
colorbar.set_label("Fluencia [protones/cm-2]")  # Label for the colorbar
# colorbar.set_label("Minutes")  # Label for the colorbar

# Show the plot
plt.show()