"""
A class for points used in the GIS Algorithms book.

History
  March 1, 2017
    More updates on __str__ to make sure integers are printed correctly.
    
  October 28, 2015
    Functions __repr__ and __str__ are updated to be more flexible and robust.

  November 10, 2015
    Add a key member to the class

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

from math import sqrt
class Point():
    """A class for points in Cartesian coordinate systems."""
    def __init__(self, x=None, y=None, key=None):
        self.x, self.y = x, y
        self.key = key
    def __getitem__(self, i):
        if i==0: return self.x
        if i==1: return self.y
        return None
    def __len__(self):
        return 2
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x==other.x and self.y==other.y
        return NotImplemented
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    def __lt__(self, other):
        if isinstance(other, Point):
            if self.x<other.x:
                return True
            elif self.x==other.x and self.y<other.y:
                return True
            return False
        return NotImplemented
    def __gt__(self, other):
        if isinstance(other, Point):
            if self.x>other.x:
                return True
            elif self.x==other.x and self.y>other.y:
                return True
            return False
        return NotImplemented
    def __ge__(self, other):
        if isinstance(other, Point):
            if self > other or self == other:
                return True
            else:
                return False
            return False
        return NotImplemented
    def __le__(self, other):
        if isinstance(other, Point):
            if self < other or self == other:
                return True
            else:
                return False
            return False
        return NotImplemented
    def __str__(self):
        """NAP: Not a point"""
        if self.x is None or self.y is None or not isinstance(self.x, (int, long, float)) or not isinstance(self.y, (int, long, float)):
            return 'NAP'
        if isinstance(self.x, (int, long)):
            fmtstr = '({0}, '
        else:
            fmtstr = '({0:.1f}, '
        if isinstance(self.y, (int, long)):
            fmtstr += '{1})'
        else:
            fmtstr += '{1:.1f})'
        return fmtstr.format(self.x, self.y)
    def __repr__(self):
        return self.__str__()
    def distance(self, other):
        return sqrt((self.x-other.x)**2 + (self.y-other.y)**2)
