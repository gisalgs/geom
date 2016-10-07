import math
from point import *
class PIPError:
    """Basic error for point-in-polygon algorithms"""
    def __init__(self, msg):
        self.message = msg

def pip_cross(point, pgon):
    """
    Determines whether a point is in a polygon. Code adopted
    from the C program in Graphics Gems IV by Haines (1994).

    Input
      pgon: a list of points as the vertices for a polygon
      point: the point

    Ouput
      Returns a boolean value of True or False and the number
      of times the half line crosses the polygon boundary

    History
       October 2016.
            pip_cross0 is removed
            changed <> to !=
            raise error if polygon is not closed (previous version modifies data)

       October 2015. A bug in previous code, pip_cross0, is fixed.
    """
    tx, ty = point.x, point.y
    if pgon[0] != pgon[-1]:
        raise PIPError('Polygon not closed')
    N = len(pgon)
    crossing = 0
    inside_flag = 0
    for i in range(N-1):
        p1, p2 = pgon[i], pgon[i+1]
        yflag1 = (p1.y >= ty)                  # p1 on or above point
        yflag2 = (p2.y >= ty)                  # p2 on or above point
        if yflag1 != yflag2:                   # p1 & p2 on two sides of half line
            xflag1 = (p1.x >= tx)              # left-right side of p1
            xflag2 = (p2.x >= tx)              # left-right side of p2
            if xflag1 == xflag2:               # p1 & p2 on same left/right side of point
                if xflag1:
                    crossing += 1
                    inside_flag = not inside_flag
            else:                              # compute intersection
                m = p2.x - float((p2.y-ty))* (p1.x-p2.x)/(p1.y-p2.y)
                if m >= tx:
                    crossing += 1
                    inside_flag = not inside_flag
        yflag1 = yflag2
    return inside_flag, crossing

if __name__ == "__main__":
    points = [ [0,10], [5,0], [10,10], [15,0], [20,10],
               [25,0], [30,20], [40,20], [45,0], [50,50],
               [40,40], [30,50], [25,20], [20,50], [15,10],
               [10,50], [8, 8], [4,50], [0,10] ]
    ppgon = [Point(p[0], p[1]) for p in points ]
    pts = [Point(10, 30), Point(10, 20),
           Point(20, 40), Point(5, 40)]
    for p in pts:
        result = pip_cross(p, ppgon)
        if result[0] == True:
            print "Point", p, "is IN"
        else:
            print "Point", p, "is OUT"

    points = [ [0,10], [5,0], [10,10], [15,0], [20,10] ]
    ppgon = [Point(p[0], p[1]) for p in points ]
    try:
        x = pip_cross(Point(10, 30), ppgon)
    except PIPError as err:
        print err.message
    else:
        print x[0]
