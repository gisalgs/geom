from overlay import *
from copy import deepcopy

d=[ Dcel(), Dcel() ]

pgon1 = [ [3,3], [9,3], [8,8], [4,8] ]
edges1 = [ [0,1], [1,2], [2,3], [3,0] ]
pgon2 = [ [1,1], [6,6], [10,2] ]
edges2 = [ [0,1], [1,2], [2,0] ]

d[0].load(pgon1, edges1)
d[1].load(pgon2, edges2)

D = Dcel()
D.hedges = d[0].hedges + d[1].hedges
D.vertices = d[0].vertices + d[1].vertices

s1 = []
for i in range(len(pgon1)-1):
    s1.append([pgon1[i], pgon1[i+1]])

s1.append([pgon1[-1], pgon1[0]])

s2 = []
for i in range(len(pgon2)-1):
    s2.append([pgon2[i], pgon2[i+1]])

s2.append([pgon2[-1], pgon2[0]])

ps1 = [Segment(i, Point(s1[i][0][0],s1[i][0][1]),
               Point(s1[i][1][0],s1[i][1][1]), 0) for i in range(len(s1))]
ps2 = [Segment(i+len(s1), Point(s2[i][0][0],s2[i][0][1]),
               Point(s2[i][1][0],s2[i][1][1]), 1) for i in range(len(s2))]
s = ps1+ps2

ints = overlay(s, D)

# get all boundary cycles
hl = deepcopy(D.hedges)
while len(hl) is not 0:
    c = []
    #print len(hl), ":",
    e0 = hl.pop()
    e = e0
    c.append(e)
    while True:
        print e, 
        e1 = e.nexthedge
        if e1 is not e0:
            c.append(e1)
            hl.remove(e1)
            e = e1
        else:
            break
    print

import pickle
pickle.dump(D, open('mydcel.pickle', 'w'))
