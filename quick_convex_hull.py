'''
Quick convex hull
https://en.wikipedia.org/wiki/Quickhull
'''

from .point import *
from .sideplr import *
from .point2line import *

def find_convex_hull(points):
    # Find the left- and right-most points in the data
    xmin = float('inf')
    xmax = -float('inf')
    for p in points:
        if p.x < xmin:
            xmin = p.x
            A = p
        if p.x > xmax:
            xmax = p.x
            B = p

    # these two points will be on the hull
    convex_hull = [A, B]
    
    # find the points on the right side of AB and put them in s1
    # find the points on the left side of AB and put them in s2
    s1 = [] 
    s2 = [] 
    for p in points[1:-2]:
        lr = sideplr(p, A, B)
        if lr > 0:
            s1.append(p)
        elif lr < 0:
            s2.append(p)

    # for each die, continuously find the point farthest from the line and add it to the hull
    # then insert that point in between the two points and do this again
    find_hull(convex_hull, s1, A, B)
    find_hull(convex_hull, s2, B, A)

    return convex_hull

def find_hull(hull: list, sk, p, q):
    '''
    Find points in sk that are on the convex hull.
    All points in sk must be on the right side of line pq
    '''

    if not sk:
        return

    # find the farthest point from the line and add it to the hull
    maxdist = -1
    C = None
    for p1 in sk:
        dist = point2line(p1, p, q)
        if dist > maxdist:
            maxdist = dist
            C = p1
    i = hull.index(p)
    hull.insert(i, C)

    # find the points on the right side of line pC, and then line Cq
    # and call this function again
    s1 = []
    s2 = []
    for p1 in sk:
        if p1 == C:
            continue
        lr = sideplr(p1, p, C)
        if lr > 0:
            s1.append(p1)
        lr = sideplr(p1, C, q)
        if lr > 0:
            s2.append(p1)
            
    find_hull(hull, s1, p, C)
    find_hull(hull, s2, C, q)

