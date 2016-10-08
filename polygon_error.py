class PolygonError:
    """Basic error for point-in-polygon algorithms"""
    def __init__(self, msg):
        self.message = msg
