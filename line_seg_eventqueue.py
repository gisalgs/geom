"""
Python classes for Event and EventQueue for the Bentley-Ottmann algorithm.

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

from point import *

class Event:
    """
    An event in the sweep line algorithm. Each Event object
    stores the event point and the line segments associated with the
    point.
    """
    def __init__(self, p=None):
        self.edges = []     # line segments associated with the event
        self.p = p          # event point
    def __repr__(self):
        return "{0}{1}".format(self.p,self.edges)
        
class EventQueue:
    """
    An event queue in the sweep line algorithm. 
    """
    def __init__(self, lset):
        """
        Constructor of EventQueue.
        Input
          lset: a list of Segment objects. The left point of
                each segment is used to create an event
        Output
          A sorted list of events as a member of this class
        """
        if lset == None:
            return
        self.events = []
        for l in lset:
            e0 = Event(l.lp)
            inx = self.find(e0)
            if inx == -1:
                e0.edges.append(l)
                self.events.append(e0)
            else:
                self.events[inx].edges.append(l)
            e1 = Event(l.rp)
            if self.find(e1) == -1:
                self.events.append(e1)
        self.events.sort(key=lambda e: e.p)

    def add(self, e):
        """
        Adds event e to the queue, updates the list of events
        """
        self.events.append(e)
        self.events.sort(key=lambda e: e.p)

    def find(self, t):
        """
        Returns the index of event t if it is in the queue. 
        Otherwise, returns -1.
        """
        if isinstance(t, Event):
            p = t.p
        elif isinstance(t, Point):
            p = t
        else: return -1
        for e in self.events:
            if p == e.p:
                return self.events.index(e)
        return -1
        
    def is_empty(self):
        return len(self.events) == 0
