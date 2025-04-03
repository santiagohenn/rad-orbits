import numpy as np
from structures import constellation
import json
import csv

folder = "ssrgt_1030_AP8"
tpo_threshold = 50.0
time_step_seconds = 5;

all_satellites = constellation.Constellation()
all_satellites.read_from_csv(f"./inputs/{folder}.csv")

# Load the NS-ND order
ND_NS = []
with open(f"./inputs/ssrgt_order.csv", "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
            ND_NS.append((int(row["ND"]), int(row["NS"])))

for sat_idx, satellite in enumerate(all_satellites.satellites):

    # I'm dealing with just one satellite each iteration but need the constellation obj to get the hash
    current_constellation = constellation.Constellation()
    current_constellation.add_satellite(satellite)
    hash = current_constellation.generate_hash_256()

    print("Processing ", ND_NS[sat_idx]," -> ", hash)

    # Load JSON data from a file
    with open(f"D:/rad-orbits/outputs/analysis/{folder}/roi_access_metrics_{hash}.json", "r") as json_file:
        data = json.load(json_file)

    # Initialize variables
    intervals = []
    start_time = None
    fluence = 0
    time = 0

    # Iterate through JSON data
    for entry in data:
        time = entry["time"]
        metric = entry["metrics"][0]  # Assuming "metrics" always has at least one element
        
        if metric >= tpo_threshold:
            fluence = fluence + metric * time_step_seconds
            if start_time is None:
                start_time = time  # Start a new interval
        else:
            if start_time is not None:
                intervals.append((start_time, time, fluence))  # End the current interval
                start_time = None
                fluence = 0

    # Handle the case where the last interval reaches the end of the data
    if start_time is not None:
        intervals.append((start_time, time, fluence))

    # Write intervals to a CSV file
    with open(f"./outputs/intervals/{folder}/access_intervals_{hash}.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["start_time", "end_time", "fluence"])  # CSV header
        writer.writerows(intervals)