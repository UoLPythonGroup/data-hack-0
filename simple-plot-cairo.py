#! /usr/bin/env python
#
# Plot all shapes contained in the "leedsAll" shapefile.
# Copyright (C) 2014 Jochen Voss <voss@seehuhn.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import cairo
import math
import shapefile

cm = 72 / 2.54
width = 29.7 * cm
height = 21 * cm
margin = .5 * cm
surface = cairo.PDFSurface("simple-plot.pdf", width, height)
ctx = cairo.Context(surface)
# move the origin to the center:
ctx.scale(1, -1)
ctx.translate(.5*width, -.5*height)

sf = shapefile.Reader("pythonGeoHack/leedsAll")
lon_min, lat_min, lon_max, lat_max = sf.bbox
lon_mid = (lon_min + lon_max) / 2
lat_mid = (lat_min + lat_max) / 2
lat_corr = math.cos(lat_mid * 2 * math.pi / 360.0)

qx = (width - 2*margin) / (lon_max - lon_min) / lat_corr
qy = (height - 2*margin) / (lat_max - lat_min)
q = min(qx, qy)

ctx.set_line_width(0.15)

edge_count = 0
for s in sf.iterShapes():
    if tuple(s.parts) != (0,):
        raise NotImplementedError("s.parts = %s" % s.parts)
    if s.shapeType != 3:
        # Shape types are explaine on page 4 of
        # http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf ,
        # type 3 means "PolyLine".
        raise NotImplementedError("s.shapetype = %s" % s.shapeType)
    if len(s.points) < 2:
        raise NotImplementedError("degenerate shape with only one point")

    edge_count += len(s.points) - 1
    for j, z in enumerate(s.points):
        x = (z[0] - lon_mid) * q * lat_corr
        y = (z[1] - lat_mid) * q
        if j == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
    ctx.stroke()
print(edge_count, "line segments")

surface.finish()
