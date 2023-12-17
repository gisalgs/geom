'''
A function testing the side of a point with respect to an oriented line

History
  December 16, 2023
    Change the use of int to directly comparing signs

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
'''

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

from .point import *

def sideplr(p, p1, p2):
    '''
    Calculates the side of point p to the vector p1p2.

    Input
      p: the point
      p1, p2: the start and end points of the line

    Output
      -1: p is on the left side of p1p2
       0: p is on the line of p1p2
       1: p is on the right side of p1p2
    '''
    lr = (p.x-p1.x)*(p2.y-p1.y)-(p2.x-p1.x)*(p.y-p1.y)
    if lr != 0:
        lr = 1 if lr>0 else -1
    return lr
    # return int((p.x-p1.x)*(p2.y-p1.y)-(p2.x-p1.x)*(p.y-p1.y))

if __name__ == "__main__":
    lr = {-1: 'left', 0: 'on the line', 1: 'right'}
    p=Point(1,1)
    p1=Point(0,0)
    p2=Point(1,0)
    print(f'Point {p} to line {p1}->{p2}: {lr[sideplr(p, p1, p2)]}')
    print(f'Point {p} to line {p2}->{p1}: {lr[sideplr(p, p2, p1)]}')
    p = Point(0.51, 0.00001)
    print(f'Point {p} to line {p1}->{p2}: {lr[sideplr(p, p1, p2)]}')
    print(f'Point {p} to line {p2}->{p1}: {lr[sideplr(p, p2, p1)]}')

    p = Point(3, 2.0001)
    p1 = Point(0, 1)
    p2 = Point(6, 3)
    print(f'Point {p} to line {p1}->{p2}: {lr[sideplr(p, p1, p2)]}')
    print(f'Point {p} to line {p2}->{p1}: {lr[sideplr(p, p2, p1)]}')
