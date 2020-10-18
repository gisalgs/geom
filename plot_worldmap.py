import matplotlib.pyplot as plt

def plot_world(points, numgraticule, numline, color=None):
    '''
    Uses the data prepared by worlmap.py to plot the world map

    The user needs to run plt.show() after calling this function.
    '''
    _, ax = plt.subplots(1, 1)
    for i in range(numline):
        if i<numgraticule:
            col = 'lightgrey'
        else:
            col = '#5a5a5a'
            if color is not None:
                col = color
        pts = [[p[1], p[2]] for p in points if p[0]==i]
        l = plt.Polygon(pts, color=col, fill=False, closed=False)
        ax.add_line(l)

    ax.axis('equal')                        # x and y one the same scale
    ax.axes.get_xaxis().set_visible(False)  # don't show axis
    ax.axes.get_yaxis().set_visible(False)  # don't show axis
    ax.set_frame_on(False)                  # no frame either
