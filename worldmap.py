from osgeo import ogr

def prep_projection_data(fname):
    points=[]
    linenum = 0
    for lat in range(-90, 91, 10):
        for lon in range(-180, 181, 10):
            points.append([linenum, lon, lat])
        linenum += 1
    
    for lon in range(-180, 181, 10):
        for lat in range(-90, -80, 1):
            points.append([linenum, lon, lat])
        for lat in range(-80, 80, 10):
            points.append([linenum, lon, lat])
        for lat in range(80, 91, 1):
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

    numline = max([p[0] for p in points]) + 1

    return points, numgraticule, numline
