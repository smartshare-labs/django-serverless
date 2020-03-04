from bson.objectid import ObjectId
from django.contrib.gis.geos import Point


def object_id():
    return str(ObjectId())


def create_point(*, lng, lat):
    return Point(lng, lat, srid=4326)
