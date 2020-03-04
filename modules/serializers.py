from rest_framework import serializers
from django.contrib.gis.geos import Point
from modules.utils import create_point


class WritePointSerializer(serializers.Serializer):
    def to_representation(self, point):
        try:
            lat, lng = float(point["lat"]), float(point["lng"])
            return {"point": Point(lat, lng, srid=4326)}
        except ValueError:
            raise serializers.ValidationError("invalid_point")


class ReadPointSerializer(serializers.Serializer):
    def to_representation(self, value):
        try:
            return {"lng": value.x, "lat": value.y}
        except ValueError:
            return None

    def to_internal_value(self, data):
        try:
            lat = float(data.get("lat"))
            lng = float(data.get("lng"))
            return create_point(lng=lng, lat=lat)
        except (ValueError, TypeError):
            raise serializers.ValidationError("invalid_point")

