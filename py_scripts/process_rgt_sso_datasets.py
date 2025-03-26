import numpy as np
from structures import constellation
import json
import csv

all_satellites = constellation.Constellation()
all_satellites.read_from_csv("./inputs/ssrgt_1030_AP8.csv")
folder = "ssrgt_1030_AP8"

tpo_threshold = 100.0

for satellite in all_satellites.satellites:

    # I'm dealing with just one satellite each iteration but need the constellation obj to get the hash
    current_constellation = constellation.Constellation()
    current_constellation.add_satellite(satellite)
    hash = current_constellation.generate_hash_256()

    print("Processing ", hash)

    # Load JSON data from a file
    with open(f"D:/rad-orbits/outputs/analysis/{folder}/roi_access_metrics_{hash}.json", "r") as json_file:
        data = json.load(json_file)

    # Initialize variables
    intervals = []
    start_time = None

    # Iterate through the JSON data
    for entry in data:
        time = entry["time"]
        metric = entry["metrics"][0]  # Assuming "metrics" always has at least one element
        
        if metric >= tpo_threshold:
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
    with open(f"./outputs/intervals/{folder}/access_intervals_{hash}.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["start_time", "end_time"])  # CSV header
        writer.writerows(intervals)