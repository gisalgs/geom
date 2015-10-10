from line_seg_intersection import *

s = [ [[20,15],[0,16]], [[3,18],[2,3]], [[4,14],[6,19]],
      [[10,17],[0,6]],  [[8,3],[5,10]], [[6,6],[11,9]],
      [[16,14],[10,6]], [[16,10],[10,11]],
      [[14,8],[16,12]] ]

psegs = [Segment(i, Point(s[i][0][0], s[i][0][1]),
                 Point(s[i][1][0], s[i][1][1]))
         for i in range(len(s))]

ints = intersections(psegs)
print "There are", len(ints), "intersection points:"
print ints
