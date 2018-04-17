from simple_geo.distance import latlng_distance

__author__ = 'sbeilin'

""" Miscellaneous geometry functions """


def bounding_box(locations):
    if locations is None or len(locations) == 0:
        return [[10, 90], [90, 10]]

    if len(locations) == 1:
        loc = locations[0]
        return [[loc.latitude - 10, loc.longitude + 10], [loc.latitude + 10, loc.longitude - 10]]

    bounds = [[0, 180], [180, 0]]

    for loc in locations:
        if loc is None:
            continue
        if loc.latitude > bounds[0][0]:
            bounds[0][0] = loc.latitude
        if loc.longitude < bounds[0][1]:
            bounds[0][1] = loc.longitude
        if loc.latitude < bounds[1][0]:
            bounds[1][0] = loc.latitude
        if loc.longitude > bounds[1][1]:
            bounds[1][1] = loc.longitude

    return bounds


def latlng_diameter(points):
    return max([latlng_distance(a, b) for a in points for b in points])
