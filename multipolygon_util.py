'''
Functions that are convenient to handle geojson polygon or multipolygons.

Change history:

    November 13, 2024 - first release

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
'''

__author__ = 'Ningchuan Xiao <ncxiao@gmail.com>'

import sys
sys.path.append('..')

from geom.point import *
from geom.point_in_polygon import *

def get_bounds(f):
    '''
    Get the bounds of a multiplygon

    INPUT
        multipoly - a polygon or multipolygon geojson object

    OUTPUT
        xmin, xmax, ymin, ymax
    '''
    def _get_bounds(a_poly):
        '''
        a_poly is a polygon that may or may not have holes:
        [ [ [x,y], [x,y], ...], [ [x,y], ...] ]
        We only needs the outter ring to get the bounds
        '''
        outter = a_poly[0]
        xcoords = [p[0] for p in outter]
        ycoords = [p[1] for p in outter]
        return min(xcoords), max(xcoords), min(ycoords), max(ycoords)

    if f['geometry']['type'] == 'Polygon':
        return _get_bounds(f['geometry']['coordinates'])
    elif f['geometry']['type'] != 'MultiPolygon':
        raise Exception('Must be a Polygon or MultiPolygon geometry')

    # initialize bounds using the coords of the first point
    xmin = xmax = f['geometry']['coordinates'][0][0][0][0]
    ymin = ymax = f['geometry']['coordinates'][0][0][0][1]

    for part in f['geometry']['coordinates']:
        x0, x1, y0, y1 = _get_bounds(part)
        xmin = min(xmin, x0)
        xmax = max(xmax, x1)
        ymin = min(ymin, y0)
        ymax = max(ymax, y1)
    
    return xmin, xmax, ymin, ymax


def point_in_multipolygon(p, muly):
    '''
    p - Point object or [x, y]
    muly - geojson multipolygon
    '''
    def _point_in_poly(p, poly):
        '''
        poly - polygon, may have holes: [ [ [x,y], [x,y]...], [ [x,y], [x,y],...] ]
        '''
        # check the outter ring
        outter = [Point(p[0], p[1]) for p in poly[0]]
        if not pip_cross(p, outter)[0]:
            return False
        for ring in poly[1:]:
            r = [Point(p[0], p[1]) for p in ring]
            if pip_cross(p, r)[0]: # if p in a ring, return false
                return False
        return True
    # if p is in any part, return true
    for part in muly['geometry']['coordinates']:
        if _point_in_poly(p, part):
            return True
    
    return False

def proj_multipoly(geo, proj_func):
    '''
    Project the entire geojson multipolygon object

    INPUT: 
        geo       - a geojson object. Only multipolygons are handled here
        proj_func - the name a function that two coordinates (x, y) and return the projected coordinates

    OUTPUT:
        proj_geo  - a projected geojson

    REQUIREMENTS
        Must have get_bounds(feature)

    EXAMPLE
        Assuming we have a geojson object loaded and it is called blkgrps:
        blkgrps_spcs = proj_multipoly(blkgrps, spcs_ohio_south)
    '''
    proj_geo = {
        'type': geo['type'], # this should be FeatureCollection
        'features': []
    }
    for f in geo['features']:
        if f['geometry']['type'] != 'MultiPolygon':
            raise Exception('Can only handle multipolygons')
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'MultiPolygon', 
                'coordinates': []},
            'properties': f['properties']
        }
        geom = []
        for part in f['geometry']['coordinates']:
            geom.append([[proj_func(p[0], p[1]) for p in ring] for ring in part])
        feature['geometry']['coordinates'] = geom
        feature['bounds'] = get_bounds(feature)
        proj_geo['features'].append(feature)
    return proj_geo
