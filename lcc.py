'''
Implementation of Lambert Conformal Conic project and its use for State Plane Ohio South.

Change history:

    November 6, 2024 - first release

# example from Snyder p 295
# LCC on sphere
# Result should have: 0.2966785, 0.2462112
R = 1
lat1 = 33
lat2 = 45
lat0 = 23
lon0 = -96
lat = 35
lon = -75
easting = 0
northing = 0

lambert_conformal_conic(lon, lat, lon0, lat0, lat1, lat2, easting, northing, R)
# (0.29667845994250686, 0.24621122933162676)

# from pyproj - but on ellipsoid
# >>> t.transform(40, -83)
# (1828420.1096133376, 728840.80764274)

spcs_ohio_south(-83, 40)
# (1828770.2861412086, 730018.3205949441)

# origin
spcs_ohio_south(-82.5, 38)
# (1968500.0, 0.0)

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
'''

__author__ = 'Ningchuan Xiao <ncxiao@gmail.com>'


from math import cos, sin, tan, radians, log, pi, e

def sec(x):
    '''Secant Function'''
    return 1/cos(x)
    
def cot(x):
    '''
    Assume lat in radians
    '''
    return 1/tan(x)


def lambert_conformal_conic(lon, lat, lon0, lat0, lat1, lat2, easting, northing, R):
    '''
    Lambert conformal conic
    formula from snyder 1987 (p 104-107)
    '''
    lon, lat, lon0, lat0, lat1, lat2 = map(radians, [lon, lat, lon0, lat0, lat1, lat2])

    n     = log(cos(lat1)/cos(lat2)) / log(tan(pi/4 + lat2/2) / tan(pi/4 + lat1/2))
    F     = cos(lat1) * tan(pi/4 + lat1/2)**n / n
    rho   = R * F / (tan(pi/4 + lat/2)**n)
    rho0  = R * F / tan(pi/4 + lat0/2)**n
    theta = n * (lon-lon0)

    x     = rho * sin(theta)
    y     = rho0 - rho * cos(theta)

    x    += easting
    y    += northing
    # msg   = f'n={n} \nF={F} \nrho={rho}\nrho0={rho0}'
    # print(msg)
    return x, y


def lambert_conformal_conic_wiki(lon, lat, lon0, lat0, lat1, lat2, easting, northing, R):
    '''
    Lambert conformal conic
    formula from wikipedia
    '''
    lon, lat, lon0, lat0, lat1, lat2 = map(radians, [lon, lat, lon0, lat0, lat1, lat2])
    n    = log(cos(lat1) * sec(lat2)) / log( tan(pi/4 + lat2/2) * cot(pi/4 + lat1/2))
    F    = cos(lat1) * tan(pi/4+lat1/2)**n / n
    rho  = R * F * cot(pi/4+lat/2)**n
    rho0 = R * F * cot(pi/4+lat0/2)**n
    x    = rho * sin(n*(lon-lon0))
    y    = rho0 - rho*cos(n*(lon-lon0))
    x   += easting
    y   += northing
    return x, y

def spcs_ohio_south(lon, lat):
    '''
    State Plane Coordinate System - Ohio South
    Unit: feet
    '''
    lon0 = -82.5
    lat0 = 38
    lat1 = 40.0333333333333
    lat2 = 38.7333333333333
    easting = 1968500
    northing = 0
    # earth radius as used in proj4 https://proj.org/en/9.4/usage/ellipsoids.html
    # converted to feet, as used in state plane
    R = 6370997.0 * 3.28084

    return lambert_conformal_conic(lon, lat, lon0, lat0, lat1, lat2, easting, northing, R)

