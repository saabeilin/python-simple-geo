import polyline
from simple_geo.point import LatLon


def encode_polyline(pts):
    return polyline.encode([(p.latitude, p.longitude) for p in pts])


def decode_polyline(encoded):
    return [LatLon(p[0], p[1]) for p in polyline.decode(encoded)]
