# Analyses distances in shapefile and plots a histogram
# Note: requires six, pyshp, matplotlib
# (NDE, 2014-07-02)

import math
import six
import shapefile
from utils import distance
import matplotlib.pyplot as plt

# Read shape data

data = shapefile.Reader("pythonGeoHack/leedsAll")
shapes = data.shapes()

# Method 1: compute distances from points

dist1 = [ sum(distance(shape.points[i], shape.points[i-1])
            for i in range(1, len(shape.points)))
              for shape in shapes ]

# Method 2: use length field of records

dist2 = [ record[2] for record in data.records() ]

# Compare methods

diff2 = 0.0
for d1, d2 in zip(dist1, dist2):
    diff2 += (d1-d2)**2

rms = math.sqrt(diff2/len(dist1))

six.print_("RMS difference = {:.3f} m".format(rms))

# Plot frequency distribution of distances

#plt.hist(dist1, bins=30, log=True)
plt.hist(dist2, bins=30, log=True)

plt.xlabel("Distance (m)")
plt.ylabel("Frequency")
plt.title("Distribution of Distances in leedsAll")
plt.grid()

plt.show()
