'''
A class for points used in the GIS Algorithms book.

Change history

  September 28, 2024

    f-strings are used now.
    Type checking for __init__.
    Convert a number in string when creating a Point object.
    Error handling.

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
        Point(1, y=12)
        Point(1, key='any attributes')
        Point(1, 2, 'any attributes')
        Point(1, 2, key='any attributes')
        Point(1, '12')
        Point('1', 12)
    '''
    # def __init__(self, x=None, y=None, key=None):
    #     self.x = x
    #     self.y = y
    #     self.key = key
    def __init__(self, *args, **kwargs): # x=None, y=None, key=None):
        '''
        Both x and y can be None. If not, they need to be numerical.

        Key is the attributes and can be of any type.

        An exception will be raised if a non-numerical value is used in either x or y.
        '''
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
            if  'y' in kwargs.keys():
                self.y = kwargs['y']
            if 'key' in kwargs.keys():
                self.key = kwargs['key']
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
            self.key = None
            if 'key' in kwargs.keys():
                self.key = kwargs['key']
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
        if self.x and not isinstance(self.x, (int, float)): 
            try:
                self.x = float(self.x)
            except Exception as e:
                print(e)
                raise Exception('XCoordinateTypeError') from None # don't traceback
        if self.y and not isinstance(self.y, (int, float)): 
            try:
                self.y = float(self.y)
            except Exception as e:
                print(e)
                raise Exception('YCoordinateTypeError') from None # don't traceback
             
    def __getitem__(self, i):
        if i==0: 
            return self.x
        if i==1: 
            return self.y
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
            return False
        return NotImplemented
    def __le__(self, other):
        if isinstance(other, Point):
            if self < other or self == other:
                return True
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
            fmtstr = f'({self.x}, '
        else:
            fmtstr = f'({self.x:.1f}, '
        if isinstance(self.y, (int)):
            fmtstr += f'{self.y})'
        else:
            fmtstr += f'{self.y:.1f})'
        return fmtstr
    def __repr__(self):
        return f'Point({self.x}, {self.y})'
    def distance(self, other):
        return sqrt((self.x-other.x)**2 + (self.y-other.y)**2)
