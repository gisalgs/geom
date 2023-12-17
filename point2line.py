import math

from .point import *

def point2line(p, p1, p2):
    """
    Calculate the distance from point to a line.
    Input
      p: the point
      p1 and p2: the two points that define a line
    Output
      d: distance from p to line p1p2
    """
    x0 = float(p.x)
    y0 = float(p.y)
    x1 = float(p1.x)
    y1 = float(p1.y)
    x2 = float(p2.x)
    y2 = float(p2.y)
    dx = x1-x2
    dy = y1-y2
    a = dy
    b = -dx
    c = y1*dx - x1*dy
    if a==0 and b==0:         # p1 and p2 are the same point
        d = math.sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0))
    else:
        d = abs(a*x0+b*y0+c)/math.sqrt(a*a+b*b)
    return d

if __name__ == "__main__":
    p, p1, p2 = Point(10,0), Point(0,100), Point(0,1)   #*@\label{point2line:l1}
    print(point2line(p, p1, p2))
    p, p1, p2 = Point(0,10), Point(1000,0.001), Point(-100,0)
    print(point2line(p, p1, p2))
    p, p1, p2 = Point(0,0), Point(0,10), Point(10,0)
    print(point2line(p, p1, p2))
    p, p1, p2 = Point(0,0), Point(10,10), Point(10,10)
    print(point2line(p, p1, p2))                         #*@\label{point2line:l2}

