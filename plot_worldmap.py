'''
Plot the world map using data prepared in worldmap.py.

History
    October 23, 2023
        Change ax.add_line to ax.add_patch

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
'''

import matplotlib.pyplot as plt

def plot_world(ax, points, numgraticule, numline, color=None):
    '''
    Uses the data prepared by worldmap.py to plot the world map.
    
    Input: 
        ax:             matplotlib axes
        points:         a list of [ [ID, X, Y], [ID, X, Y], ...]
        numgraticule:   the number of lines forming the graticule
        numline:        the total number of line IDs
        color:          if not None, the color used to draw coastlines (default: #5a5a5a)

    The user needs to import matplotlib.pyplot first and run plt.show() after calling this function.
    '''

    for i in range(numline):
        if i<numgraticule:
            col = 'lightgrey'
        else:
            col = '#5a5a5a'
            if color is not None:
                col = color
        pts = [[p[1], p[2]] for p in points if p[0]==i]
        l = plt.Polygon(pts, color=col, fill=False, closed=False)
        ax.add_patch(l)

    ax.axis('equal')                       # x and y one the same scale
    ax.axes.get_xaxis().set_visible(False)  # don't show axis
    ax.axes.get_yaxis().set_visible(False)  # don't show axis
    ax.set_frame_on(False)                  # no frame either
