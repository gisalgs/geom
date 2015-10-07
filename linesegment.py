from point import *
from sideplr import *

## Two statuses of the left endpoint
ENDPOINT = 0   ## original left endpoint
INTERIOR = 1   ## interior in the segment

class Segment:
    """
    A class for line segments.
    """
    def __init__(self, e, p0, p1, c=None):
        """
        Constructor of Segment class.
        Input
          e: segment ID, an integer
          p0, p1: endpoints of segment, Point objects
        """
        if p0>=p1:
            p0,p1 = p1,p0           # p0 is always left
        self.edge = e               # ID, in all edges
        self.lp = p0                # left point
        self.lp0 = p0               # original left point  #*@\label{lineseg:lp0}
        self.rp = p1                # right point
        self.status = ENDPOINT      # status of segment
        self.c = c                  # c: feature ID
    def __eq__(self, other):
        if isinstance(other, Segment):
            return (self.lp==other.lp and self.rp==other.rp)\
                or (self.lp==other.rp and self.rp==other.lp)
        return NotImplemented
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    def __lt__(self, other): 
        if isinstance(other, Segment):
            if self.lp and other.lp:
                lr = sideplr(self.lp, other.lp, other.rp)
                if lr == 0:
                    lrr = sideplr(self.rp, other.lp, other.rp)
                    if other.lp.x < other.rp.x:
                        return lrr > 0
                    else:
                        return lrr < 0
                else:
                    if other.lp.x > other.rp.x:
                        return lr < 0
                    else:
                        return lr > 0
        return NotImplemented
    def __gt__(self, other):
        result = self.__lt__(other)
        if result is NotImplemented:
            return result
        return not result
    def __repr__(self):
        return "{0}".format(self.edge)
    def contains(self, p):
        """
        Returns none zero if segment has p as an endpoint
        """
        if self.lp == p:
            return -1
        elif self.rp == p:
            return 1
        else:
            return 0
