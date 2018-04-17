def gpx_from_points(points):
    gpx = """<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0"
xmlns="http://www.topografix.com/GPX/1/0" creator="Lab-m - www.lab-m.ru"
xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">
"""

    gpx += "<trk>"
    gpx += "<trkseg>"
    for p in points:
        gpx += '<trkpt lat="' + str(p.latitude) + '" lon="' + str(p.longitude) + '">'
        gpx += '<time>' + str(p.time.strftime('%Y-%m-%dT%H:%M:%SZ')) + '</time>'
        gpx += '</trkpt>'
    gpx += '</trkseg>'
    gpx += "</trk>"

    gpx += "</gpx>"

    return gpx
