"""
A Python program for the Mollweide projection.

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

from numpy import pi, cos, sin, radians, degrees, sqrt

def opt_theta(lat, verbose=False):
    """
    Finds optimal theta value using Newton-Raphson iteration.
    Input
      lat: the latitude value
      verbose: True to print intermediate output
    Output
      theta
    """
    lat1 = radians(lat)
    theta = lat1
    while True:
        dtheta = -(theta+sin(theta)-
                   pi*sin(lat1))/(1.0+cos(theta))
        if verbose:
            print("theta =", degrees(theta))
            print("delta =", degrees(dtheta))
        if int(1000000*dtheta) == 0:
            break
        theta = theta+dtheta
    return theta/2.0

def transform2(lon, lat, lon0=0, R=1.0):
    """
    Returns the transformation of lon and lat
    on the Mollweide projection.

    Input
      lon: longitude
      lat: latitude
      lon0: central meridian
      R: radius of the globe

    Output
      x: x coordinate (origin at 0,0)
      y: y coordinate (origin at 0,0)
    """
    lon1 = lon-lon0
    if lon0 != 0:
        if lon1>180:
            lon1 = -((180+lon0)+(lon1-180))
        elif lon1<-180:
            lon1 = (180-lon0)-(lon1+180)
    theta = opt_theta(lat)
    x = sqrt(8.0)/pi*R*lon1*cos(theta)
    x = radians(x)
    y = sqrt(2.0)*R*sin(theta)
    return x, y
