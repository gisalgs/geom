from line_seg_intersection import *
from dcel import *

class OvearlayError(Exception): pass

def update_intersect_dcel(hl, e):
    """
    Updates the hedges related to e given a hedge list hl
    """
    l = len(hl)
    if l<2:
        raise OvearlayError(
            "Overlay/DCEL error: single edge for vertex")
    big, small = l-1, 0  
    for i in range(l):
        if e.angle > hl[i].angle:
            big,small = i-1,i
            break
    b,s = hl[big], hl[small]
    e.prevhedge = b.twin
    e.twin.nexthedge = s
    b.prevhedge = e.twin
    b.twin.nexthedge = e
    s.prevhedge = e.twin

def handle_edge_vertex(L, R, C, p, D):
    e = C[0].edge
    v1 = Vertex(C[0].lp0.x, C[0].lp0.y)# get the hedges for e
    v2 = Vertex(C[0].rp.x, C[0].rp.y)
    e1, e2 = D.findhedges(v1, v2)      # origins: ends of e
    e3 = Hedge(v1, Vertex(p.x, p.y))   # hedge, p as origin
    e4 = Hedge(v2, Vertex(p.x, p.y))   # hedge, p as origin
    # updating around endpoints of e:
    e1.twin = e3
    e3.twin = e1
    e2.twin = e4
    e4.twin = e2
    e3.nexthedge = e2.nexthedge
    e4.nexthedge = e1.nexthedge
    
    v = D.findvertex(p)                # updating around p
    v.sortincident()
    hl = v.hedgelist
    update_intersect_dcel(v.hedgelist, e3)
    update_intersect_dcel(v.hedgelist, e4)
    # add two new hedges with p as origin
    v.hedgelist.append(e3)
    v.hedgelist.append(e4)
    # e1, e2 updated in D due to references
    D.hedges.append(e3)
    D.hedges.append(e4)

def handle_edge_edge(L, R, C, p, D):
    pass

def handle_vertex_vertex(L, R, C, p, D):
    pass

def overlay(psegs, D):
    """
    Overlays polygons from two maps.
    Input
      psegs: a list of Segments. The c attribute in each
             segment indicates the source map
      D: a partial DCEL with the original hedges and vertices
    Output
      intpoints: list of intersection points
    """
    eq = EventQueue(psegs)
    intpoints = []
    T = AVLTree()
    L=[]
    while not eq.is_empty():   # for all events
        e = eq.events.pop(0)   # remove the event
        p = e.p                # event point
        L = e.edges            # segments with p as left end
        R,C = get_edges(T, p)  # Intersection at p among L+R+C
        if len(L+R+C) > 1:
            for s in L+R+C:
                if not s.contains(p):
                    s.lp = p
                    s.status = INTERIOR
            intpoints.append(p)
            R,C = get_edges(T, p)
            c1 = (L+R+C)[0].c
            cross = False
            for l in L+R+C:
                if c1 is not l.c:
                    cross = True
                    break
            # Update its vertices and edge lists
            if cross is True:
                if len(C) == 1:  # CASE 1: edge passes vertex
                    handle_edge_vertex(L, R, C, p, D)
                if len(C) > 1:   # CASE 2: edge crosses edge
                    handle_edge_edge(L, R, C, p, D)
                if len(C) == 0:  # CASE 3: vertex on vertex
                    handle_vertex_vertex(L, R, C, p, D)
        for s in R+C:
            T.discard(s)
        for s in L+C:
            T.insert(s, 1)
        if len(L+C) == 0:
            s = R[0]
            if s is not None:
                sl, sr = get_lr(T, s)
                y = find_new_event(sl, sr, p, eq)
        else:
            lp, lpp = get_lrmost(T, L+C) 
            try:
                sl = T.prev_key(lp)
            except KeyError:           # only on last key
                sl = None
            try:
                sr = T.succ_key(lpp)
            except KeyError:           # only on last key
                sr = None
            find_new_event(sl, lp, p, eq)
            find_new_event(sr, lpp, p, eq)
    return intpoints
