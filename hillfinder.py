# Finds the biggest hill in the leedsRoads.geojson dataset
# (NDE, 2014-07-03)

import json
import webbrowser
import matplotlib.pyplot as plt
from utils import great_circle_distance

# Grab data from file

with open("pythonGeoHack/leedsRoads.geojson", "rt") as infile:
    data = json.loads(infile.read())

# Find feature with biggest elevation change

maxdiff = 0.0
elevations = []
hill = None

for feature in data["features"]:

    # Convert elevation CSV to list of numbers, ignoring suspect last item

    csv = feature["properties"]["elevtns"]
    elev = [ float(item) for item in csv.split(",")[:-1] ]

    # Keep track of biggest elevation change

    diff = max(elev) - min(elev)
    if diff > maxdiff:
        maxdiff = diff
        elevations = elev
        hill = feature

# Display OSM data for the hill in a browser

way_id = int(hill["properties"]["id"])

url = "http://www.openstreetmap.org/way/{:d}".format(way_id)

webbrowser.open(url)

# Accumulate horizontal distances

points = hill["geometry"]["coordinates"][:-1]

assert len(points) == len(elevations)  # sanity check

dist = 0.0
distances = [dist]
for i in range(1, len(points)):
    dist += great_circle_distance(points[i], points[i-1])
    distances.append(dist)

# Plot elevation vs distance using matplotlib

plt.plot(distances, elevations)

plt.xlabel("Horizontal distance (m)")
plt.ylabel("Elevation (m)")
title = "Way ID: {:d}".format(way_id)
plt.title(title)
plt.grid()

plt.show()
