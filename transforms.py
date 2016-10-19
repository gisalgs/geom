"""
A Python program for the sinusoidal and equirectangular projections.

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

from numpy import cos, radians

def transform_sinusoidal(lon, lat, lon0=0):
    """
    Returns the transformation of lon and lat on the Sinusoidal projection.

    Input
      lon: longitude in degrees
      lat: latitude in degrees
      lon0: central meridian in degrees

    Output
      x: x coordinate (origin at 0,0)
      y: y coordinate (origin at 0,0)
    """
    lon1 = lon-lon0
    x = lon1 * cos(radians(lat))
    y = lat
    return x, y

def transform_equirectangular(lon, lat, lat0=0):
    """
    Returns the transformation of lon and lat on the equirectangular projection,
    a.k.a. the equidistant cylindrical projection, geographic projection, or la
    carte parallelogrammatique projection. It is a special case of the plate carree
    projection

    Input
      lon: longitude in degrees
      lat: latitude in degrees (will not be used)
      lat0: standard parallel in degrees (true scale)

    Output
      x: x coordinate (origin at 0,0)
      y: y coordinate (origin at 0,0)

    """
    x = lon * cos(radians(lat0))
    y = lat
    return x, y
