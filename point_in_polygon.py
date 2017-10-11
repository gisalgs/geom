'''
Determines whether a point is in a polygon. Code adopted
from the C program in Graphics Gems IV by Haines (1994).

Change history
    October 10, 2017
        Use generic Python exception

    September 2017
        Python 3

    December 2016
        Add pip_cross2, which also works for complicated polygons
        with multiple parts or holes

    October 2016
        Removed function pip_cross0
        Changed <> to !=
        Raise error if polygon is not closed (previous version modifies data)
            This requires polygon_error.py.
        Changed some variable names for better read

   October 2015
        A bug in previous code, pip_cross0, is fixed.
'''

import math
import sys
sys.path.append('..')
from geom.point import *

# from geom.polygon_error import PolygonError

def pip_cross(point, pgon):
    """
    Input
      pgon:   a list of points as the vertices for a polygon
              The polygon needs to be closed. Otherwise an error is raised.
      point:  the point

    Ouput
      Returns a boolean value of True or False and the number
      of times the half line crosses the polygon boundary
    """
    # tx, ty = point.x, point.y
    x, y = point.x, point.y
    if pgon[0] != pgon[-1]:
        raise Exception('Polygon not closed')
    N = len(pgon)
    crossing_count = 0
    is_point_inside = False
    for i in range(N-1):
        p1, p2 = pgon[i], pgon[i+1]
        yside1 = (p1.y >= y)
        yside2 = (p2.y >= y)
        if yside1 != yside2:
            xside1 = (p1.x >= x)
            xside2 = (p2.x >= x)
            if xside1 == xside2:
                if xside1:
                    crossing_count += 1
                    is_point_inside = not is_point_inside
            else:
                m = p2.x - (p2.y-y)*(p1.x-p2.x)/float(p1.y-p2.y)
                if m >= x:
                    crossing_count += 1
                    is_point_inside = not is_point_inside
    return is_point_inside, crossing_count

def pip_cross2(point, polygons):
    """
    Input
      polygon: a list of lists, where each inner list contains points
               forming a part of a multipolygon. Each part must be
               closed, otherwise an error will be raised.
      point:   the point

    Ouput
      Returns a boolean value of True or False and the number
      of times the half line crosses the polygon boundary
    """
    # tx, ty = point.x, point.y
    x, y = point.x, point.y
    crossing_count = 0
    is_point_inside = False
    for pgon in polygons:
        if pgon[0] != pgon[-1]:
            raise Exception('Polygon not closed')
        N = len(pgon)
        for i in range(N-1):
            p1, p2 = pgon[i], pgon[i+1]
            yside1 = (p1.y >= y)
            yside2 = (p2.y >= y)
            if yside1 != yside2:
                xside1 = (p1.x >= x)
                xside2 = (p2.x >= x)
                if xside1 == xside2:
                    if xside1:
                        crossing_count += 1
                        is_point_inside = not is_point_inside
                else:
                    m = p2.x - (p2.y-y)*(p1.x-p2.x)/float(p1.y-p2.y)
                    if m >= x:
                        crossing_count += 1
                        is_point_inside = not is_point_inside
    return is_point_inside, crossing_count


if __name__ == "__main__":
    points = [ [0,10], [5,0], [10,10], [15,0], [20,10],
               [25,0], [30,20], [40,20], [45,0], [50,50],
               [40,40], [30,50], [25,20], [20,50], [15,10],
               [10,50], [8, 8], [4,50], [0,10] ]
    ppgon = [Point(p[0], p[1]) for p in points ]
    pts = [Point(10, 30), Point(10, 20),
           Point(20, 40), Point(5, 40)]
    for p in pts:
        result = pip_cross2(p, [ppgon])
        if result[0] == True:
            print("Point", p, "is IN")
        else:
            print("Point", p, "is OUT")

    points = [ [0,10], [5,0], [10,10], [15,0], [20,10] ]
    ppgon = [Point(p[0], p[1]) for p in points ]
    try:
        x = pip_cross2(Point(10, 30), [ppgon])
    except Exception as err:
        print(err)
    else:
        print(x[0])

    # a polygon with holes
    points1 = [ [0,0], [6,0], [5,4], [3,4], [2,3], [0,3], [1,2], [0,0]]
    points2 = [ [4,1], [3,3], [5,2], [5,1], [4,1] ]
    points3 = [ [1,1], [2,2], [3,1], [1,1]]
    polygon = [[Point(p[0], p[1]) for p in plg] for plg in [points1, points2, points3]]
    pts = [[1,1], [2,2], [4,2], [1,2.1], [0,2], [3,1.5], [2.5,1.5], [4,1], [5,2], [3,3], [2,1.1]]
    pts = [Point(p[0], p[1]) for p in pts]
    print([pip_cross2(p, polygon)[0] for p in pts])
