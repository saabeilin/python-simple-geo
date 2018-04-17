import uuid


class LatLon:
    def __init__(self, lat: float, lon: float, name=None):
        self.id = str(uuid.uuid4())
        self.longitude = float(lon)
        self.latitude = float(lat)
        self.name = name

    def __eq__(self, other):
        return (self.latitude == other.latitude and
                self.longitude == other.longitude and
                self.name == other.name)

    # A dirty hack to make it hashable in case of a custom comparator:
    __hash__ = object.__hash__

    def __repr__(self):
        return "LatLon (%s,%s) [%s]" % (self.latitude, self.longitude, (self.name or "")[:20])

    def simple_object(self, *args, **kwargs) -> dict:
        """
        Returns a 'simple object' (aka 'python json' or 'pyson') representation,
        to conform to SimpleObjectMixin protocol
        Args:
            args: unused
            kwargs: unused
        """
        return {
            'type': 'LatLon',
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'name': self.name
        }
