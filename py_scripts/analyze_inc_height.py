import csv
from structures import constellation
import numpy as np

constellation_incs = range(0, 100, 5)
constellation_heights = range(300 + 6371, 2000 + 6371, 200)

all_satellites = constellation.Constellation()
all_satellites.read_from_csv("./inputs/ssrgt_single.csv")

scenario_timespan_ms = 777600 * 1000

output_metrics = []

for inc_idx, inc in enumerate(constellation_incs):
    for sma_idx, sma in enumerate(constellation_heights):

        for satellite in all_satellites.satellites:
            satellite.inclination = inc
            satellite.semi_major_axis = sma
        
        hash = all_satellites.generate_hash_256()

        # Load intervals from CSV
        intervals = []
        with open(f"E:/rad-orbits/outputs/intervals/access_intervals_{hash}.csv", "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                intervals.append((int(row["start_time"]), int(row["end_time"])))

        # Ensure intervals are sorted
        intervals.sort()

        if len(intervals) == 0 and sma > (6371 + 800):
            intervals.append([0, scenario_timespan_ms])
        else:
            intervals.append([0, 0])

        # Compute interval durations and waiting times
        durations = [end - start for start, end in intervals]
        waiting_times = [intervals[i][0] - intervals[i - 1][1] for i in range(1, len(intervals))]

        # Compute metrics
        metrics = {
            "inc": inc,
            "sma": sma,
            "percentage_of_access": ( sum(durations) / scenario_timespan_ms ),
            "min_duration": min(durations) if durations else None,
            "max_duration": max(durations) if durations else None,
            "avg_duration": sum(durations) / len(durations) if durations else None,
            "min_waiting_time": min(waiting_times) if waiting_times else 0,
            "max_waiting_time": max(waiting_times) if waiting_times else 0,
            "avg_waiting_time": sum(waiting_times) / len(waiting_times) if waiting_times else 0,
            "frequency": len(intervals),  # Number of intervals
        }

        #output_metrics.append([inc, metrics["percentage_of_access"], metrics["avg_duration"], metrics["min_waiting_time"], metrics["max_waiting_time"]])
        #output_metrics.append(metrics)
        output_metrics.append(metrics)

# Save all metrics to CSV
output_file = "./outputs/metrics_summary_single_ssrgt.csv"
with open(output_file, "w", newline="") as csv_file:
    fieldnames = [
        "inc",
        "sma",
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