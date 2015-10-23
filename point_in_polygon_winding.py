import math
from point import *

def is_left(p, p1, p2):
    """
    Tests if point p is to the left of a line segement
    between p1 and p2
    Output
       0  the point is on the line
      >0  p is to the left of the line
      <0  p is to the right of the line
    """
    return (p2.x-p1.x)*(p.y-p1.y) - (p.x-p1.x)*(p2.y-p1.y)

def pip_wn(point, pgon):
    """
    Determines whether a point is in a polygon using the 
    winding number algorithm using trigonometric functions. 
    Code adopted from the C program in Graphics Gems IV
    (Haines 1994).
    Input
      point: the point
      pgon: a list of points as the vertices for a polygon
    Ouput
      Returns a boolean value of True or False and the number
      of times the half line crosses the polygon boundary
    """
    if pgon[0] != pgon[-1]:
        pgon.append(pgon[0])
    n = len(pgon)
    xp = point.x
    yp = point.y
    wn = 0
    for i in range(n-1):
        xi = pgon[i].x
        yi = pgon[i].y
        xi1 = pgon[i+1].x
        yi1 = pgon[i+1].y
        thi = (xp-xi)*(xp-xi1) + (yp-yi)*(yp-yi1)
        norm = (math.sqrt((xp-xi)**2+(yp-yi)**2) 
                * math.sqrt((xp-xi1)**2+(yp-yi1)**2))
        if thi != 0:
            thi = thi/norm
        thi = math.acos(thi)
        wn += thi
    wn /= 2*math.pi
    wn = int(wn)
    return wn is not 0, wn

def pip_wn1(point, pgon):
    """
    Determines whether a point is in a polygon using the 
    winding number algorithm without trigonometric functions.
    Code adopted from the C program in Graphics Gems IV 
    (Haines 1994).
    Input
      point: the point
      pgon: a list of points as the vertices for a polygon
    Ouput
      Returns a boolean value of True or False and the number
      of times the half line crosses the polygon boundary
    """
    wn = 0
    n = len(pgon)
    for i in range(n-1):
        if pgon[i].y <= point.y:
            if pgon[i+1].y > point.y:
                if is_left(point, pgon[i], pgon[i+1])>0:
                    wn += 1
        else:
            if pgon[i+1].y <= point.y:
                if is_left(point, pgon[i], pgon[i+1])<0:
                    wn -= 1
    return wn is not 0, wn

if __name__ == "__main__":
    pgon = [ [2,3], [7,4], [6,6], [4,2], [11,5],
             [5,11], [2,3] ]
    point = Point(6, 4)
    ppgon = [Point(p[0], p[1]) for p in pgon ]
    print pip_wn(point, ppgon)
    print pip_wn1(point, ppgon)
