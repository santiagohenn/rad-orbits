import numpy as np
from structures import constellation
import json
import csv

constellation_incs = range(0, 100, 5)
constellation_heights = range(300 + 6371, 2000 + 6371, 200)

all_satellites = constellation.Constellation()
all_satellites.read_from_csv("./inputs/ssrgt_single.csv")

tpo_threshold = 10.0

for inc_idx, inc in enumerate(constellation_incs):
    for sma_idx, sma in enumerate(constellation_heights):

        for satellite in all_satellites.satellites:
            print(satellite)
            satellite.inclination = inc
            satellite.semi_major_axis = sma
    
        hash = all_satellites.generate_hash_256()

        print("Processing ",inc_idx, hash)

        # Load JSON data from a file
        with open(f"E:/rad-orbits/outputs/analysis/roi_access_metrics_{hash}.json", "r") as json_file:
            data = json.load(json_file)

        # Initialize variables
        intervals = []
        start_time = None

        # Iterate through the JSON data
        for entry in data:
            time = entry["time"]
            metric = entry["metrics"][0]  # Assuming "metrics" always has at least one element
            
            if metric > tpo_threshold:
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
        with open(f"E:/rad-orbits/outputs/intervals/access_intervals_{hash}.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["start_time", "end_time"])  # CSV header
            writer.writerows(intervals)

        #print(constellation)

# 2025-01-01T16:00:00.000,6771567,0,29.954,341.464,0.000,359.737