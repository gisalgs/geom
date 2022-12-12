'''
A class for points used in the GIS Algorithms book.

Change history
  December 10, 2022
    Now use *args and **kwargs in __init__ to make it more flexible

  September 30, 2017
    Change __repr__ to return a new string like 'Point(x,y)'

  April 24, 2017
    Remove long from isinstance. Python 3 no longer support long

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
'''

__author__ = 'Ningchuan Xiao <ncxiao@gmail.com>'

from math import sqrt

class Point:
    '''
    A class for points in Cartesian coordinate systems.

    Examples: 
    
    A Point object at (10, 1) with an attribute of 100 can be created using the following:

        Point(10, 1, 100) 
        Point(x=10, y=1, key=100)

    These are also valid examples:
    
        Point(10)
        Point(10, 1)
        Point(x=10, y=1)
    
    '''
    # def __init__(self, x=None, y=None, key=None):
    #     self.x = x
    #     self.y = y
    #     self.key = key
    def __init__(self, *args, **kwargs): # x=None, y=None, key=None):
        self.x = None
        self.y = None
        self.key = None
        if len(args) == 1:
            if isinstance(args[0], (list, tuple)):
                if len(args[0]) == 2:
                    self.x = args[0][0]
                    self.y = args[0][1]
            else:
                self.x = args[0]
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
            self.key = None
        elif len(args) == 3:
            self.x = args[0]
            self.y = args[1]
            self.key = args[2]
        else:
            if 'x' in kwargs.keys():
                self.x = kwargs['x']
            if  'y' in kwargs.keys():
                self.y = kwargs['y']
            if 'key' in kwargs.keys():
                self.key = kwargs['key']
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
    def isvalid(self):
        if not isinstance(self.x, (int, float)) \
                or not isinstance(self.y, (int, float)):
            return False
        return True
    def __str__(self):
        '''NaP: Not a point'''
        if not self.isvalid():
            return 'NaP'
        if isinstance(self.x, (int)):
            fmtstr = '({0}, '
        else:
            fmtstr = '({0:.1f}, '
        if isinstance(self.y, (int)):
            fmtstr += '{1})'
        else:
            fmtstr += '{1:.1f})'
        return fmtstr.format(self.x, self.y)
    def __repr__(self):
        return 'Point({}, {})'.format(self.x, self.y)
    def distance(self, other):
        return sqrt((self.x-other.x)**2 + (self.y-other.y)**2)
