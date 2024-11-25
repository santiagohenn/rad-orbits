import numpy as np
from structures import constellation

constellation_incs = range(45, 100, 1)
labels = [f'{inc} [°]' for inc in constellation_incs]
max_mean_tput = np.zeros(len(constellation_incs))
max_peak_tput = np.zeros(len(constellation_incs))

constellation = constellation.Constellation()
constellation.read_from_csv("./inputs/satellites.csv")

for inc_idx, inc in enumerate(constellation_incs):

    for satellite in constellation.satellites:
        satellite.inclination = inc
    
    hash = constellation.generate_hash_256()
    print(constellation)
    print(inc_idx, hash)

# 2025-01-01T16:00:00.000,6771567,0,29.954,341.464,0.000,359.737