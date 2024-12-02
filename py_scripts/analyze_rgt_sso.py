import csv
from structures import constellation
import numpy as np

folder = "ssrgt_1030"
scenario_timespan_ms = 777600 * 1000

all_satellites = constellation.Constellation()
all_satellites.read_from_csv(f"./inputs/{folder}.csv")

# Load the NS-ND order
ND_NS = []
with open(f"./inputs/ssrgt_order.csv", "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
            ND_NS.append((int(row["ND"]), int(row["NS"])))

output_metrics = []

for sat_idx, satellite in enumerate(constellation.satellites):

    # I'm dealing with just one satellite but need the constellation obj to get the hash
    current_constellation = constellation.Constellation()
    current_constellation.add_satellite(satellite)
    hash = current_constellation.generate_hash_256()

    print("Analizing ", hash)

    # Load intervals from CSV
    intervals = []
    with open(f"./outputs/intervals/{folder}/access_intervals_{hash}.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            intervals.append((int(row["start_time"]), int(row["end_time"])))

    # Ensure intervals are sorted
    intervals.sort()

    # Compute interval durations and waiting times
    durations = [end - start for start, end in intervals]
    waiting_times = [intervals[i][0] - intervals[i - 1][1] for i in range(1, len(intervals))]

    # Compute metrics
    metrics = {
        "ND": ND_NS[sat_idx][0],
        "NS": ND_NS[sat_idx][1],
        "height": satellite.semi_major_axis - 6371,
        "inc": satellite.inclination, 
        "percentage_of_access": ( sum(durations) / scenario_timespan_ms ),
        "min_duration": min(durations) if durations else None,
        "max_duration": max(durations) if durations else None,
        "avg_duration": sum(durations) / len(durations) if durations else None,
        "min_waiting_time": min(waiting_times) if waiting_times else None,
        "max_waiting_time": max(waiting_times) if waiting_times else None,
        "avg_waiting_time": sum(waiting_times) / len(waiting_times) if waiting_times else None,
        "frequency": len(intervals),  # Number of intervals
    }

    #output_metrics.append([inc, metrics["percentage_of_access"], metrics["avg_duration"], metrics["min_waiting_time"], metrics["max_waiting_time"]])
    #output_metrics.append(metrics)
    output_metrics.append(metrics)

# Save all metrics to CSV
output_file = f"./outputs/metrics_summary_{folder}.csv"
with open(output_file, "w", newline="") as csv_file:
    fieldnames = [
        "ND",
        "NS",
        "height",
        "inc",
        "percentage_of_access",
        "min_duration",
        "max_duration",
        "avg_duration",
        "min_waiting_time",
        "max_waiting_time",
        "avg_waiting_time",
        "frequency",
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_metrics)