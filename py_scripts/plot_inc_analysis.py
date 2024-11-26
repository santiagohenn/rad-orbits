import pandas as pd
import matplotlib.pyplot as plt

# Load the metrics CSV
metrics_file = "./outputs/metrics_summary.csv"
data = pd.read_csv(metrics_file)

# Define the metrics to plot
metric_1 = "avg_duration"          # Example: Second metric to plot (optional)

# Plot avg time within rad zone
plt.figure(figsize=(10, 6))

# First metric
plt.plot(data["inc"], data[metric_1] / 1000.0, label="Average time within radiation zone", marker="o", linestyle="--")

# Customize plot
plt.title("Metrics Plot")
plt.xlabel("Inclination [degrees]")
plt.ylabel("Time [s]")
plt.xticks(rotation=45, ha="right")  # Rotate file names for better readability
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

