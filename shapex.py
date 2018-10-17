'''
A class and related functions that handle reading of shapefiles

It now only supports four types of shapefile:
    Point, MultiPoint (not tested), PolyLine, Polygon.

History

    October 9, 2017
        Support slicing!

    October 8, 2017
        First version.
        Supports four types.
        No slicing

Credit: the read_dbf method is adopted from http://code.activestate.com/recipes/362715/

Author
    Ningchuan Xiao
    ncxiao@gmail.com
'''

from struct import unpack, calcsize
from os.path import isfile
from datetime import date

shapefile_types = {
  0: 'Null Shape',
  1: 'Point',
  3: 'PolyLine',
  5: 'Polygon',
  8: 'MultiPoint',
  11: 'PointZ',
  13: 'PolyLineZ',
  15: 'PolygonZ',
  18: 'MultiPointZ',
  21: 'PointM',
  23: 'PolyLineM',
  25: 'PolygonM',
  28: 'MultiPointM',
  31: 'MultiPatch'
}

supported_types = [ 'Point', 'MultiPoint', 'PolyLine', 'Polygon' ]

def clockwise(polygon):
    '''calculate 2*A
    polygon: [ [x, y], [x, y], ... ]

    polygon = [ [1, 0], [2,0], [2,2], [1,2], [1, 0] ]
    clockwise(polygon) # False
    polygon.reverse()
    clockwise(polygon) # True
    '''
    if polygon[0] != polygon[-1]:
        return
    num_point = len(polygon)
    A = 0
    for i in range(num_point-1):
        p1 = polygon[i]
        p2 = polygon[i+1]
        ai = p1[0] * p2[1] - p2[0] * p1[1]
        A += ai
    return A<0

class shapex:
    '''
    A class for points in Cartesian coordinate systems.

    Examples

    >>> fname = '/Users/xiao/lib/gisalgs/data/uscnty48area.shp'
    >>> shp = shapex(fname)
    >>> print(shp[60])
    '''
    def __init__(self, fname):
        if not fname.endswith('.shp'):
            raise Exception('Need a .shp file.')
        self.fname_shp = fname
        self.fname_shx = fname[:-3]+'shx'
        self.fname_dbf = fname[:-3]+'dbf'
        if not isfile(self.fname_shp) or not isfile(self.fname_shx) or not isfile(self.fname_dbf):
            raise Exception('Need at least three files: .shp, .shx, .dbf')
        self.open_shapefile()

    def open_shapefile(self):
        self.f_shx = open(self.fname_shx, 'rb')
        h1 = unpack('>7i', self.f_shx.read(28))
        h2 = unpack('<2i 8d', self.f_shx.read(72))
        file_length = h1[-1]
        self.num_rec = (file_length-50)//4

        self.f_shp = open(self.fname_shp, 'rb')
        h1 = unpack('>7i', self.f_shp.read(28))     # BIG
        h2 = unpack('<2i 8d', self.f_shp.read(72))  # LITTLE

        self.file_length = h1[-1]
        self.version = h2[0]
        self.shape_type = shapefile_types[h2[1]]
        # self.xmin, self.ymin, self.xmax, self.ymax, self.zmin, self.zmax, self.mmin, self.mmax = h2[2:10]
        self.xmin = h2[2]
        self.ymin = h2[3]
        self.xmax = h2[4]
        self.ymax = h2[5]
        self.zmin = h2[6]
        self.zmax = h2[7]
        self.mmin = h2[8]
        self.mmax = h2[9]
        self.this_feature_num = 0
        # get (offset, content length) pairs from shx
        # remember each record has a header of 8 bytes
        index = unpack('>'+'i'*self.num_rec*2, self.f_shx.read(self.num_rec*4*4))
        self.index = [(index[i]*2, index[i+1]*2) for i in range(0, len(index), 2)]

        # get schema, etc.
        self.f_dbf = open(self.fname_dbf, 'rb')
        dbf_numrec, lenheader = unpack('<xxxxLH22x', self.f_dbf.read(32))
        self.numfields = (lenheader - 33) // 32
        if dbf_numrec != self.num_rec:
            raise Exception('SHP and DBF have different numbers of records')
        self.fields = []
        for fieldno in range(self.numfields):
            name, dtype, size, deci = unpack('<11sc4xBB14x', self.f_dbf.read(32))
            name = name.replace(b'\0', b'')       # take out \x00
            self.fields.append((name.decode('ascii'), dtype.decode('ascii'), size, deci))
        self.f_dbf.read(1) # skip the terminator
        self.fields.insert(0, ('DeletionFlag', 'C', 1, 0))
        self.formatstr = ''.join(['%ds' % fieldinfo[2] for fieldinfo in self.fields])
        self.formatsize = calcsize(self.formatstr)
        self.dbf_header_length = 32 + 32*self.numfields + 1

    def __getitem__(self, i):
        if not self.shape_type in supported_types:
            raise Exception(self.shape_type + ' shape type not supported')
        if isinstance(i, slice):
            return [self[j] for j in range(*i.indices(len(self)))]
        elif isinstance(i, int):
            if i<0:
                i = self.num_rec + i
            if i<0 or i+1>self.num_rec:
                raise Exception('Feature index out of range (' + str(i) + ')')
            pos = self.index[i]
            self.f_shp.seek(pos[0] + 8) # skip record hearder, which is not useful

            if self.shape_type == 'Polygon':
                feature = self.readpolygon()
            if self.shape_type == 'PolyLine':
                feature = self.readpolygon()
                if feature['geometry']['type'] == 'MultiPolygon':
                    feature['geometry']['type'] = 'MultiLineString'
                else:
                    feature['geometry']['type'] = 'LineString'
            if self.shape_type == 'Point':
                feature = self.readpoint()
            if self.shape_type == 'MultiPoint':
                feature = self.readmultipoint()

            # get properties here.
            properties = self.read_dbf(i)
            feature['properties'] = properties
            feature['id'] = i
            return feature
        else:
            raise TypeError('Invalid index')

    def read_dbf(self, i):
        # Note: dtypes of D, L are note tested
        self.f_dbf.seek(self.dbf_header_length + i * self.formatsize)
        record = unpack(self.formatstr, self.f_dbf.read(self.formatsize))
        if record[0] == ' ':
            return ' ' * self.formatsize
        result = []
        for (name, dtype, size, deci), value in zip(self.fields, record):
            value = value.decode('ascii')
            if name == 'DeletionFlag':
                continue
            if dtype == 'N':
                value = value.replace('\0', '').lstrip()
                if value == '':
                    value = 0
                elif deci:
                    value = float(value)
                else:
                    value = int(value)
            elif dtype == 'C':
                value = value.rstrip()
            elif dtype == 'D':
                y, m, d = int(value[:4]), int(value[4:6]), int(value[6:8])
                value = date(y, m, d)
            elif dtype == 'L':
                value = (value in 'YyTt' and 'T') or (value in 'NnFf' and 'F') or '?'
            elif dtype == 'F':
                value = float(value)
            result.append(value)
        properties = {}
        for fi in range(1, len(self.fields)):
            properties[self.fields[fi][0]] = result[fi-1]
        return properties

    def readpoint(self):
        point = unpack('<idd', self.f_shp.read(4+8+8))
        feature = {
            "type": "Feature",
            "geometry": {
                "type": 'Point',
                "coordinates": (point[1], point[2])
            }
        }
        return feature

    def readmultipoint(self):
        # This function is not tested
        content_head = unpack('<i 4d i', self.f_shp.read(40))
        shape_type = content_head[0]
        num_points = content_head[5]
        points = unpack('<'+'d'*num_points*2, self.f_shp.read(8*2*num_points))
        multipoints = [(points[i], points[i+1]) for i in range(0, len(points), 2)]
        feature = {
            "type": "Feature",
            "geometry": {
                "type": 'MultiPoint',
                "coordinates": multipoints
            }
        }
        return feature

    def readpolygon(self):
        content_head = unpack('<i 4d 2i', self.f_shp.read(44))
        shape_type = content_head[0]
        num_parts = content_head[5]
        num_points = content_head[6]
        parts = unpack('<'+'i'*num_parts, self.f_shp.read(4*num_parts))
        points = unpack('<'+'d'*num_points*2, self.f_shp.read(8*2*num_points))
        feature = {
            "type": "Feature",
            "geometry": {
                "type": 'Polygon'
            }
        }
        if num_parts == 1:
            polygon = [[(points[i], points[i+1]) for i in range(0, len(points), 2)]]
            feature['geometry']['coordinates'] = polygon
        else:
            directions = []
            polygons = []
            for j in range(num_parts):
                start = parts[j]*2
                if j != num_parts-1:
                    end = parts[j+1]*2
                else:
                    end = len(points)
                polygon = [(points[i], points[i+1]) for i in range(start, end, 2)]
                polygons.append(polygon)
                directions.append(clockwise(polygon))
            if False in directions:
                feature['geometry']['type'] = 'Polygon'
                feature['geometry']['coordinates'] = polygons
            else:
                feature['geometry']['type'] = 'MultiPolygon'
                multipolygon = []
                for poly in polygons:
                    multipolygon.append([poly])
                feature['geometry']['coordinates'] = multipolygon
        return(feature)

    def __len__(self):
        return self.num_rec
    def __iter__(self):
        return self
    def __next__(self):
        if self.this_feature_num >= self.num_rec:
            self.this_feature_num = 0
            raise StopIteration
        feature = self.__getitem__(self.this_feature_num)
        self.this_feature_num += 1
        return feature
    def close(self):
        self.f_shp.close()
        self.f_shx.close()
        self.f_dbf.close()

    @property
    def bounds(self):
        return(self.xmin, self.ymin, self.xmax, self.ymax)

    @property
    def schema(self):
        myschema = {}
        myschema['geometry'] = self.shape_type
        properties = []
        for fi in range(1, len(self.fields)):
            name = self.fields[fi][0]
            f1 = self.fields[fi][1]
            f2 = self.fields[fi][2]
            dci = self.fields[fi][3]
            if f1 == 'C':
                fmt = 'str:' + str(f2)
            elif f1 == 'F':
                fmt = 'float:' + str(f2) + '.' + str(dci)
            elif f1 == 'N':
                if dci == 0:
                    fmt = 'int:' + str(f2)
                else:
                    fmt = 'float:' + str(f2) + '.' + str(dci)
            elif f1 == 'D':
                fmt = 'datetime'
            else:
                fmt = 'other'
            properties.append((name, fmt))
        myschema['properties'] = properties
        return myschema

if __name__ == '__main__':
    fname = '/Users/xiao/lib/gisalgs/data/uscnty48area.shp'
    # fname = '/Users/xiao/lib/gisalgs/data/ne_110m_coastline.shp'
    # fname = '/Users/xiao/lib/gisalgs/data/ne_110m_populated_places.shp'
    shp = shapex(fname)
    print('Shape type:', shp.shape_type)
    print(shp.schema)
    print(shp.bounds)
    for f in shp:
        pass
    # print(shp[60])
    # print(shp[100])
    print(len(shp[12:17]))
    shp.close()
