# Various utility functions
# (NDE, 2014-07-02)

from math import radians, sqrt, sin, cos, atan2


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
