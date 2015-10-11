"""
Test drive for the sinusoidal and equirectangular projections.

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""
__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

from osgeo import ogr
import matplotlib.pyplot as plt
from transforms import *
from worldmap import *

fname = '../data/ne_110m_coastline.shp'
pp, numgraticule, numline = prep_projection_data(fname)

points=[]
for p in pp:
    p1 = transform_sinusoidal(p[1], p[2])
    points.append([p[0], p1[0], p1[1]])

frame = plt.gca()
for i in range(numline):
    if i<numgraticule:
        col = 'lightgrey'
    else:
        col = '#5a5a5a'
    ptsx = [p[1] for p in points if p[0]==i]
    ptsy = [p[2] for p in points if p[0]==i]
    l = plt.Line2D(ptsx, ptsy, color=col)
    frame.add_line(l)

plt.axis('scaled')
frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)
frame.set_frame_on(False)
frame.set_frame_on(True)
plt.show()
