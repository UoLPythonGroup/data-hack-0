# Analyses distances in shapefile and plots a histogram
# Note: requires six, pyshp, matplotlib
# (NDE, 2014-07-02)

import six
import shapefile
from math import radians, sqrt, sin, cos, atan2
import matplotlib.pyplot as plt


MEAN_EARTH_RADIUS = 6.371009e+06


def distance(p, q):
    """
    Returns the great circle distance between points p and q.

    Vincenty's formula is used.  p and q are (lon, lat) pairs, with
    longitude and latitude expressed in degrees.  Distance is in metres.
    """

    phi1 = radians(p[1])
    phi2 = radians(q[1])

    lambda1 = radians(p[0])
    lambda2 = radians(q[0])
    delta = abs(lambda1 - lambda2)

    top = sqrt((cos(phi2)*sin(delta))**2 +
     (cos(phi1)*sin(phi2) - sin(phi1)*cos(phi2)*cos(delta))**2)

    bottom = sin(phi1)*sin(phi2) + cos(phi1)*cos(phi2)*cos(delta)

    return MEAN_EARTH_RADIUS*atan2(top, bottom)


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

rms = sqrt(diff2/len(dist1))

six.print_("RMS difference = {:.3f} m".format(rms))

# Plot frequency distribution of distances

#plt.hist(dist1, bins=30, log=True)
plt.hist(dist2, bins=30, log=True)

plt.xlabel("Distance (m)")
plt.ylabel("Frequency")
plt.title("Distribution of Distances in leedsAll")
plt.grid()

plt.show()
