from rest_framework import serializers
from modules.serializers import WritePointSerializer


class ThreadSerializer(serializers.Serializer):
    some_value = serializers.CharField()
    # start_location = WritePointSerializer()


class TestSerializer(serializers.Serializer):
    echo = serializers.BooleanField()
