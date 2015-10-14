"""
Line segment intersections using the Bentley-Ottmann Algorithm.

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

from bintrees import AVLTree
from point import *
from intersection import *
from line_seg_eventqueue import *

def get_edges(t, p):
    """
    Gets the edges that contain point p as their right
    endpoint or in the interior
    """
    lr = []
    lc = []
    for s in AVLTree(t):
        if s.rp == p:
            lr.append(s)
        elif s.lp == p and s.status == INTERIOR:
            lc.append(s)
        elif sideplr(p, s.lp, s.rp) == 0:
            lc.append(s)
    return lr, lc

def get_lr(T, s):
    """
    Returns the left and right neighbors (branches) of s in T.
    """
    try:
        sl = T.floor_key(s)
    except KeyError:
        sl = None
    try:
        sr = T.ceiling_key(s)
    except KeyError:
        sr = None
    return sl, sr

def get_lrmost(T, segs):
    """
    Finds the leftmost and rightmost segments of segs in T
    """
    l = []
    for s in list(T):
        if s in segs:
            l.append(s)
    if len(l) < 1:
        return None, None
    return l[0], l[-1]

def find_new_event(s1, s2, p, q):
    """
    Tests if s1 intersects s2 at a point that is not in the event queue.
    When a new intersection point is found, a new event will be created
    and added to the event queue.

    Input:
       s1: line segment
       s2: line segment
       p: the point of the current event
       q: event queue

    Output:
       True if a new point is found, False otherwise

    Change: the content in the queue (q) may change.
    """
    ip = intersectx(s1, s2)
    if ip is None:
        return False
    if q.find(ip) is not -1:
        return False
    if ip.x>p.x or (ip.x==p.x and ip.y >= p.y):
        e0 = Event()
        e0.p = ip
        e0.edges = [s1, s2]
        q.add(e0)
    return True

def intersectx(s1, s2):
    """
    Tests intersection of 2 input segments. If intersection is possible,
    the actual intersection point will be calculated and returned.
    """
    if not test_intersect(s1, s2):
        return None
    p = getIntersectionPoint(s1, s2)   # an intersection
    return p

def intersections(psegs):
    """
    Implementation of the Bentley-Ottmann algorithm.

    Input
      psegs: a list of segments

    Output
      intpoints: a list of intersection points
    """
    eq = EventQueue(psegs)
    intpoints = []
    T = AVLTree()
    L=[]
    while not eq.is_empty():            # for all events
        e = eq.events.pop(0)            # remove the event
        p = e.p                         # get event point
        L = e.edges                     # segments with p as left end
        R,C = get_edges(T, p)           # p: right (R) and interior (C)
        if len(L+R+C) > 1:              # Intersection at p among L+R+C
            for s in L+R+C:
                if not s.contains(p):   # if p is interior
                    s.lp = p            # change lp and
                    s.status = INTERIOR # status 
            intpoints.append(p)
            R,C = get_edges(T, p)
        for s in R+C:
            T.discard(s)
        for s in L+C:
            T.insert(s, str(s))
        if len(L+C) == 0:
            s = R[0]
            if s is not None:
                sl, sr = get_lr(T, s)
                find_new_event(sl, sr, p, eq)
        else:
            sp, spp = get_lrmost(T, L+C)
            try:
                sl = T.prev_key(sp)
            except KeyError:            # only on last key
                sl = None
            try:
                sr = T.succ_key(spp)
            except KeyError:            # only on last key
                sr = None
            find_new_event(sl, sp, p, eq)
            find_new_event(sr, spp, p, eq)
    return intpoints
