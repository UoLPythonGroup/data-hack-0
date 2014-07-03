# Extracts distance measuremens from leedsRoads.geojson
# and plots a histogram - compare with distance1.py
# (NDE, 2014-07-02)

import json
import matplotlib.pyplot as plt

# Grab data from file

with open("pythonGeoHack/leedsRoads.geojson", "rt") as infile:
    data = json.loads(infile.read())

# Extract distances

distances = [ feature["properties"]["lngthMt"]
               for feature in data["features"] ]

# Plot frequency distribution

plt.hist(distances, bins=30, log=True)

plt.xlabel("Distance (m)")
plt.ylabel("Frequency")
plt.title("Distribution of Distances in leedsRoads.geojson")
plt.grid()

plt.show()
