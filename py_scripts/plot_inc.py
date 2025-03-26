import pandas as pd
import matplotlib.pyplot as plt

# Load the metrics CSV
metrics_file = "./outputs/metrics_summary.csv"
data = pd.read_csv(metrics_file)

# Define the metrics to plot
metric_1 = "percentage_of_access"          # Example: Second metric to plot (optional)

# Plot avg time within rad zone
plt.figure(figsize=(10, 6))

# First metric
plt.plot(data["inc"], data[metric_1] * 100, label="Percentage of time within rad zone", marker="o", linestyle="--")

# Customize plot
plt.title("Access to rad zone")
plt.xlabel("Inclination [degrees]")
plt.ylabel("Percentage [%]")
plt.xticks(rotation=45, ha="right")  # Rotate file names for better readability
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

