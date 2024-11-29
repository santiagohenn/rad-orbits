import numpy as np
from structures import constellation
import json
import csv

constellation_incs = range(45, 100, 1)

constellation = constellation.Constellation()
constellation.read_from_csv("./inputs/satellites.csv")

for inc_idx, inc in enumerate(constellation_incs):

    for satellite in constellation.satellites:
        satellite.inclination = inc
    
    hash = constellation.generate_hash_256()

    print("Processing ",inc_idx, hash)

    # Load JSON data from a file
    with open(f"./outputs/analysis/750km/roi_access_metrics_{hash}.json", "r") as json_file:
        data = json.load(json_file)

    # Initialize variables
    intervals = []
    start_time = None

    # Iterate through the JSON data
    for entry in data:
        time = entry["time"]
        metric = entry["metrics"][0]  # Assuming "metrics" always has at least one element
        
        if metric == 1.0:
            if start_time is None:
                start_time = time  # Start a new interval
        else:
            if start_time is not None:
                intervals.append((start_time, time))  # End the current interval
                start_time = None

    # Handle the case where the last interval reaches the end of the data
    if start_time is not None:
        intervals.append((start_time, data[-1]["time"]))

    # Write intervals to a CSV file
    with open(f"./outputs/intervals/750km/access_intervals_{hash}.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["start_time", "end_time"])  # CSV header
        writer.writerows(intervals)

    #print(constellation)

# 2025-01-01T16:00:00.000,6771567,0,29.954,341.464,0.000,359.737