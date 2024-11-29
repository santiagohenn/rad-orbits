import csv
from structures import constellation
import numpy as np

constellation_incs = range(45, 100, 1)

constellation = constellation.Constellation()
constellation.read_from_csv("./inputs/satellites.csv")

scenario_timespan_ms = 777600 * 1000
                       # 777600000
                       # 23567340000
output_metrics = []

for inc_idx, inc in enumerate(constellation_incs):

    for satellite in constellation.satellites:
        satellite.inclination = inc
    
    hash = constellation.generate_hash_256()

    # Load intervals from CSV
    intervals = []
    with open(f"./outputs/intervals/750km/access_intervals_{hash}.csv", "r") as csv_file:
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
        "inc": inc,
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
output_file = "./outputs/metrics_summary_750.csv"
with open(output_file, "w", newline="") as csv_file:
    fieldnames = [
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