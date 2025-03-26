import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the metrics CSV
metrics_file = "./outputs/metrics_summary_single_ssrgt.csv"
data = pd.read_csv(metrics_file)

# Filter data for heatmap (height and inc only)
filtered_data = data[["sma", "inc", "percentage_of_access"]]

# Create a pivot table for the heatmap
pivot_data = filtered_data.pivot_table(
    index="sma",  # Rows correspond to orbit height
    columns="inc",   # Columns correspond to inclination
    values="percentage_of_access",  # Heatmap values
    aggfunc="mean"   # Aggregate multiple values by their mean
)

# Create the heatmap
plt.figure(figsize=(10, 8))
heatmap = sns.heatmap(
    pivot_data * 100,  # Convert percentage to [0, 100] scale
    cmap="rocket",        # Use the 'jet' colormap
    cbar_kws={"label": "Perc. of Access [%]", "shrink": 0.5},
    square=True        # Make the cells square
)

plt.gca().invert_yaxis()

# Add labels and title
plt.xlabel("Inclination [°]")
plt.ylabel("Orbit Height [km]")
plt.title(r"$\text{Percentage of access to a} > 10.00 \, \text{MeV cm}^{-2} \, \text{s}^{-1} \, \text{region}$ for a LEO")

# Show the heatmap
plt.tight_layout()
plt.show()