import math

from simple_geo.distance import latlng_distance, cross_talk_distance, poly_length

DEBUG = False


# #
# # TODO: see also
# https://github.com/sebleier/RDP/blob/master/__init__.py
# https://github.com/fhirschmann/rdp/blob/master/rdp/__init__.py
# #


def simplify_points(pts, tolerance):
    anchor = 0  # begin index
    floater = len(pts) - 1  # end index

    stack = []
    keep = set()

    stack.append((anchor, floater))  # границы точек для для применения алгоритма
    while stack:
        anchor, floater = stack.pop()

        # initialize line segment
        if pts[floater] != pts[anchor]:
            anchorX = float(pts[floater].latitude - pts[anchor].latitude)  # расстояние по оси X
            anchorY = float(pts[floater].longitude - pts[anchor].longitude)  # расстояние по оси Y
            seg_len = math.sqrt(anchorX ** 2 + anchorY ** 2)
            # если в результате вычисления seg_len == машинному 0, то произойдёт ошибка деления на 0
            try:
                # формируем единичный вектор направления
                anchorX /= seg_len
                anchorY /= seg_len
            except Exception:
                anchorX = anchorY = seg_len = 0.0
        else:
            anchorX = anchorY = seg_len = 0.0

        # inner loop:
        max_dist = 0.0
        farthest = anchor + 1
        for i in range(anchor + 1, floater):
            dist_to_seg = 0.0
            # compare to anchor
            vecX = float(pts[i].latitude - pts[anchor].latitude)
            vecY = float(pts[i].longitude - pts[anchor].longitude)
            seg_len = math.sqrt(vecX ** 2 + vecY ** 2)
            # dot product:
            proj = vecX * anchorX + vecY * anchorY
            if proj < 0.0:
                dist_to_seg = seg_len
            else:
                # compare to floater
                vecX = float(pts[i].latitude - pts[floater].latitude)
                vecY = float(pts[i].longitude - pts[floater].longitude)
                seg_len = math.sqrt(vecX ** 2 + vecY ** 2)
                # dot product:
                proj = vecX * (-anchorX) + vecY * (-anchorY)
                if proj < 0.0:
                    dist_to_seg = seg_len
                else:  # calculate perpendicular distance to line (pythagorean theorem):
                    dist_to_seg = math.sqrt(abs(seg_len ** 2 - proj ** 2))
                if max_dist < dist_to_seg:
                    max_dist = dist_to_seg
                    farthest = i

        if max_dist <= tolerance:  # use line segment
            keep.add(anchor)
            keep.add(floater)
        else:
            stack.append((anchor, farthest))
            stack.append((farthest, floater))

    keep = list(keep)
    keep.sort()
    data = [pts[i] for i in keep]
    return data


RDP_MAX_DEPTH = 15


def simplify_rdp(points, epsilon=None, depth=0):
    """
    Simplifies a polyline using a RDP algorithm
    @param points:
    @return:
    """
    if not epsilon:
        epsilon = (max(poly_length(points), 10)) * 0.025

    if DEBUG:
        print("RDP initial:", len(points))
        print("tolerance:", epsilon)

    dmax = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = cross_talk_distance(points[i], points[0], points[-1]) \
            if latlng_distance(points[0], points[-1]) > epsilon \
            else latlng_distance(points[i], points[0])
        if d > dmax:
            index = i
            dmax = d
    if dmax >= epsilon and depth < RDP_MAX_DEPTH:
        results = simplify_rdp(points[:index + 1], epsilon, depth + 1)[:-1] + simplify_rdp(points[index:], epsilon,
                                                                                           depth + 1)
    else:
        results = [points[0], points[index], points[-1]]

    if DEBUG:
        print("RDP result:", len(results))

    return results
