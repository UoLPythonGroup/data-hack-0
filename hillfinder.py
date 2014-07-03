# Finds the biggest hill in the leedsRoads.geojson data
# (NDE, 2014-07-02)

import json
import webbrowser
import matplotlib.pyplot as plt
from utils import distance

# Grab data from file

with open("pythonGeoHack/leedsRoads.geojson", "rt") as infile:
    data = json.loads(infile.read())

# Find feature with biggest elevation change

maxdiff = 0.0
hill_elev = []
hill = None

for feature in data["features"]:
    csv = feature["properties"]["elevtns"]
    elev = [ float(item) for item in csv.split(",")[:-1] ]  # ignore last item
    diff = max(elev) - min(elev)
    if diff > maxdiff:
        maxdiff = diff
        hill_elev = elev
        hill = feature

# Display OSM data for the hill in a browser

way_id = int(hill["properties"]["id"])

url = "http://www.openstreetmap.org/way/{:d}".format(way_id)

webbrowser.open(url)

# Accumulate horizontal distances

points = hill["geometry"]["coordinates"][:-1]

assert len(points) == len(hill_elev)  # sanity check

d = 0
dist = [0.0]
for i in range(1, len(points)):
    d += distance(points[i], points[i-1])
    dist.append(d)

# Plot elevation vs distance using matplotlib

plt.plot(dist, hill_elev)

plt.xlabel("Horizontal distance (m)")
plt.ylabel("Elevation (m)")
title = "Way ID: {:d}".format(way_id)
plt.title(title)
plt.grid()

plt.show()
