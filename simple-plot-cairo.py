#! /usr/bin/env python

import cairo
import math
import shapefile

sf = shapefile.Reader("pythonGeoHack/leedsAll")
shapes = sf.shapes()

width = 8.0 * 72
height = 8.0 * 72
surface = cairo.PDFSurface("map.pdf", width, height)
ctx = cairo.Context(surface)

lon_min, lat_min, lon_max, lat_max = sf.bbox

lon_mid = (lon_min + lon_max) / 2
lat_mid = (lat_min + lat_max) / 2
r = 6371
x_range = (lat_max - lat_min) / 360.0 * 2 * math.pi * r * math.cos(lat_mid * 2 * math.pi / 360.0)
y_range = (lon_max - lon_min) / 360.0 * 2 * math.pi * r
scale = min(width / x_range, height / y_range)

# move the origin to the center
ctx.scale(1, -1)
ctx.translate(.5*width, -.5*height)

ctx.set_line_width(0.1)

qx = 1500 * math.cos(lat_mid * 2 * math.pi / 360.0)
qy = 1500

edge_count = 0
node_count = 0
for s in shapes:
    if tuple(s.parts) != (0,):
        raise NotImplementedError("s.parts = %s" % s.parts)
    if s.shapeType != 3:
        raise NotImplementedError("s.shapetype = %s" % s.shapeType)
    if len(s.points) < 2:
        raise NotImplementedError("degenerate shape with only one point")

    node_count += len(s.points)
    edge_count += len(s.points) - 1
    for j, x in enumerate(s.points):
        if j == 0:
            ctx.move_to((x[0] - lon_mid)*qx, (x[1]-lat_mid)*qy)
        else:
            ctx.line_to((x[0] - lon_mid)*qx, (x[1]-lat_mid)*qy)
    ctx.stroke()

surface.finish()

print(node_count, "nodes")
print(edge_count, "edges")
