from point import *

def sideplr(p, p1, p2):
    """
    Calculates the side of point p to the vector p1p2.
    Input
      p: the point
      p1, p2: the start and end points of the line
    Output
      -1: p is on the left side of p1p2
       0: p is on the line of p1p2
       1: p is on the right side of p1p2
    """
    return int((p.x-p1.x)*(p2.y-p1.y)-(p2.x-p1.x)*(p.y-p1.y))

if __name__ == "__main__":
    p=Point(1,1)
    p1=Point(0,0)
    p2=Point(1,0)
    print "Point %s to line %s->%s: %d"%(
        p, p1, p2, sideplr(p, p1, p2))
    print "Point %s to line %s->%s: %d"%(
        p, p2, p1, sideplr(p, p2, p1))
    p = Point(0.5, 0)
    print "Point %s to line %s->%s: %d"%(
        p, p1, p2, sideplr(p, p1, p2))
    print "Point %s to line %s->%s: %d"%(
        p, p2, p1, sideplr(p, p2, p1))

