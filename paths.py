'''
Functions that help create a Path object in matplotlib
'''

from matplotlib.path import Path
from matplotlib.patches import PathPatch

def path_codes(n):
    codes = [Path.LINETO for i in range(n)]
    codes[0] = Path.MOVETO
    return codes

def make_path(lines):
    '''Creates a matplotlib path.

    This function requires the following:
       from matplotlib.path import Path
       def path_codes

    Input:
       lines: [ [[x,y], [x,y],... ], [[x,y], [x,y],... ], [ [x,y], [x,y],... ] ]
                ----- exterior ----  ---- interior ----- ...
    Output:
       path: a Path object'''
    verts = []
    for line in lines:
        verts.extend(line)
    codes = path_codes(len(lines[0]))
    for line in lines[1:]:
        codes += path_codes(len(line))
    path = Path(verts, codes)
    return path

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from geom.point import *
    from geom.point_in_polygon import *
    import matplotlib.pyplot as plt

    points1 = [ [0,0], [6,0], [5,4], [3,4], [2,3], [0,3], [1,2], [0,0]]
    points2 = [ [4,1], [3,3], [5,2], [5,1], [4,1] ]
    points3 = [ [1,1], [2,2], [3,1], [1,1]]

    polygon = [[Point(p[0], p[1]) for p in plg] for plg in [points1, points2, points3]]

    pts = [[1,1], [2,2], [4,2], [1,2.1], [0,2], [3,1.5], [2.5,1.5], [4,1], [5,2], [3,3], [2,1.1]]
    pts = [Point(p[0], p[1]) for p in pts]

    inout = lambda pip: 1 if pip is True else 0

    results = [inout(pip_cross2(p, polygon)[0]) for p in pts]

    path = make_path([points1] + [points2] + [points3])
    patch = PathPatch(path, facecolor='#AAAAAA', edgecolor='grey', alpha=0.5)

    ax = plt.gca()
    ax.add_patch(patch)

    colors = [['red', 'blue'][i] for i in results]
    l2 = plt.scatter([p.x for p in pts], [p.y for p in pts], color=colors, s=15)
    labels = ['p%s'%(i+1) for i in range(len(pts))]
    for i, p in enumerate(pts):
        plt.text(p.x+0.1, p.y, labels[i], color='red')

    ax.set_aspect(1)
    plt.grid()

    plt.show()
