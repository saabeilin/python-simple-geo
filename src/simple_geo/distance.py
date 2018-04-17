import math

R = 6378137  # earth radius in meters
d2r = math.pi / 180


def latlng_distance(this, other):
    dLat = (other.latitude - this.latitude) * d2r
    dLon = (other.longitude - this.longitude) * d2r
    lat1 = this.latitude * d2r
    lat2 = other.latitude * d2r
    sin1 = math.sin(dLat / 2)
    sin2 = math.sin(dLon / 2)

    a = sin1 * sin1 + sin2 * sin2 * math.cos(lat1) * math.cos(lat2)

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def cross_talk_distance(this, other1, other2):
    """
    Calculates the cross-talk distance between `this` and a `line` from other1 to other2
    See: http://stackoverflow.com/a/20369652/1360276
    @param this:
    @param other1:
    @param other2:
    @return:
    """

    # φ is latitude, λ is longitude, R is earth radius
    # bearingAC = atan2( sin(Δλ)*cos(φ₂), cos(φ₁)*sin(φ₂) − sin(φ₁)*cos(φ₂)*cos(Δλ) )
    # bearingAB = atan2( sin(Δλ)*cos(φ₂), cos(φ₁)*sin(φ₂) − sin(φ₁)*cos(φ₂)*cos(Δλ) )

    y2 = math.sin(other2.longitude * d2r - this.longitude * d2r) * math.cos(other2.latitude * d2r)
    x2 = math.cos(this.latitude * d2r) * math.sin(other2.latitude * d2r) - math.sin(this.latitude * d2r) * math.cos(
        other2.latitude * d2r) * math.cos(other2.latitude * d2r - this.latitude * d2r)
    bearing2 = math.atan2(y2, x2)

    y1 = math.sin(other1.longitude * d2r - this.longitude * d2r) * math.cos(other1.latitude * d2r)
    x1 = math.cos(this.latitude * d2r) * math.sin(other1.latitude * d2r) - math.sin(this.latitude * d2r) * math.cos(
        other1.latitude * d2r) * math.cos(other1.latitude * d2r - this.latitude * d2r)
    bearing1 = math.atan2(y1, x1)

    dLon = other2.longitude * d2r - this.longitude * d2r

    # distanceAC = acos( sin(φ₁)*sin(φ₂) + cos(φ₁)*cos(φ₂)*cos(Δλ) )*R
    distanceAC = math.acos(
        math.sin(this.latitude * d2r) * math.sin(other2.latitude * d2r) + math.cos(this.latitude * d2r) * math.cos(
            other2.latitude * d2r) * math.cos(dLon))
    # distance = asin(sin(distanceAC/ R) * sin(bearingAC − bearing AB)) * R
    min_distance = math.fabs(math.asin(math.sin(distanceAC) * math.sin(bearing1 - bearing2))) * R

    return min_distance


def poly_length(points):
    d = 0
    for i in range(len(points) - 1):
        d += latlng_distance(points[i], points[i + 1])
    return d


def max_distance(point, points):
    return max([latlng_distance(point, p) for p in points])


def min_distance(point, points):
    return min([latlng_distance(point, p) for p in points])
