from rest_framework import serializers


class PetSerializer(serializers.Serializer):
    pet_id = serializers.CharField(source="external_id", read_only=True)
    name = serializers.CharField()

class ListPetSerializer(serializers.Serializer):
    pet_id = serializers.CharField(source="external_id", read_only=True)
    name = serializers.CharField(read_only=True)
