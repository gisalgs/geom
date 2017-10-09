'''
A function calculating the centroid and area of a polygon

Change history
   October 2017
        Raise a generic exception. PolygonError in polygon_error no longer needed.

   September 2017
        Python 3!

   October 2016.
        Changed some variable names for better read.
        Raise error if polygon is not closed (previous version modifies data)
        This requires polygon_error.py.

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
'''

import sys
sys.path.append('..')
from geom.point import *
# from geom.polygon_error import PolygonError

def centroid(polygon):
    '''
    Calculates the centroid and area of a polygon.

    Input
      pgon: a list of Point objects

    Output
      A: the area of the polygon
      C: the centroid of the polygon
    '''
    if polygon[0] != polygon[-1]:
        # raise PolygonError('Polygon not closed')
        raise Exception('Polygon not closed')
    num_point = len(polygon)
    A = 0
    xmean = 0
    ymean = 0
    for i in range(num_point-1):
        p1 = polygon[i]
        p2 = polygon[i+1]
        ai = p1.x * p2.y - p2.x * p1.y
        A += ai
        xmean += (p2.x + p1.x) * ai
        ymean += (p2.y + p1.y) * ai
    A = A/2.0
    C = Point(xmean/(6*A), ymean/(6*A))
    return abs(A), C

# TEST
if __name__ == "__main__":
    points = [ [0,10], [5,0], [10,10], [15,0], [20,10],
               [25,0], [30,20], [40,20], [45,0], [50,50],
               [40,40], [30,50], [25,20], [20,50], [15,10],
               [10,50], [8, 8], [4,50], [0,10] ]
    polygon = [ Point(p[0], p[1]) for p in points ]

    print(centroid(polygon))

    try:
        x = centroid(polygon[:-1])
    except Exception as err:
        print(err)
    else:
        print(x)

    polygon.reverse()
    print(centroid(polygon))
