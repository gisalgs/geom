"""
Prepares data for projection transformation.

History
  October 6, 2016
    Added default parameters for lat and lon bounds

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""
from osgeo import ogr

def prep_projection_data(fname, lon0=-180, lon1=181, lat0=-90, lat1=91):
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
