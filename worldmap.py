"""
Prepares data for projection transformation.

History
    February 28, 2018
        Shapex is default

    October 10, 2017
        Now supports both shapex and OGR

    October 6, 2016
        Added default parameters for lat and lon bounds

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

# assume shapex.py is stored in a folder called mapping
import sys
sys.path.append('..')
from mapping.shapex import *

try:
    from osgeo import ogr
except ImportError:
    use_lib = 'SHAPEX'
else:
    use_lib = 'OGR'

def prep_projection_data_ogr(fname, lon0=-180, lon1=181, lat0=-90, lat1=91):
    points=[]
    linenum = 0
    for lat in range(lat0, lat1, 10):
        for lon in range(lon0, lon1, 10):
            points.append([linenum, lon, lat])
        linenum += 1

    for lon in range(lon0, lon1, 10):
        for lat in range(lat0, lat1, 10):
            points.append([linenum, lon, lat])
        linenum += 1

    numgraticule = linenum

    driveName = "ESRI Shapefile"
    driver = ogr.GetDriverByName(driveName)
    vector = driver.Open(fname, 0)
    layer = vector.GetLayer(0)

    for i in range(layer.GetFeatureCount()):
        f = layer.GetFeature(i)
        geom = f.GetGeometryRef()
        for i in range(geom.GetPointCount()):
            p = geom.GetPoint(i)
            points.append([linenum, p[0], p[1]])
        linenum += 1

    # numline = max([p[0] for p in points]) + 1

    return points, numgraticule, linenum

def prep_projection_data_shapex(fname, lon0=-180, lon1=181, lat0=-90, lat1=91):
    points=[]
    linenum = 0
    for lat in range(lat0, lat1, 10):
        for lon in range(lon0, lon1, 10):
            points.append([linenum, lon, lat])
        linenum += 1

    for lon in range(lon0, lon1, 10):
        for lat in range(lat0, lat1, 10):
            points.append([linenum, lon, lat])
        linenum += 1

    numgraticule = linenum

    shpdata = shapex(fname)
    for f in shpdata:
        geom = f['geometry']['coordinates']
        for p in geom[0]:
            points.append([linenum, p[0], p[1]])
        linenum += 1

    return points, numgraticule, linenum

def prep_projection_data(fname, lon0=-180, lon1=181, lat0=-90, lat1=91, _use_lib='SHAPEX'):
    if use_lib =='OGR' and _use_lib == 'OGR':
        return prep_projection_data_ogr(fname, lon0, lon1, lat0, lat1)
    else:
        return prep_projection_data_shapex(fname, lon0, lon1, lat0, lat1)

if __name__ == '__main__':
    fname = '../data/ne_110m_coastline.shp'
    raw_points, numgraticule, numline = prep_projection_data(fname)
    print(len(raw_points))
    print(numgraticule, numline)
    print(raw_points[0])
    print(raw_points[3000])
