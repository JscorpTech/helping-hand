from rest_framework import serializers

from ...models import PositionModel


class BasePositionSerializer(serializers.ModelSerializer):
    long = serializers.SerializerMethodField()
    lat = serializers.SerializerMethodField()

    def get_lat(self, obj):
        return obj.location.x

    def get_long(self, obj):
        return obj.location.y

    class Meta:
        model = PositionModel
        exclude = [
            "location",
            "user",
        ]


class ListPositionSerializer(BasePositionSerializer):
    class Meta(BasePositionSerializer.Meta): ...


class RetrievePositionSerializer(BasePositionSerializer):
    class Meta(BasePositionSerializer.Meta): ...


class CreatePositionSerializer(BasePositionSerializer):
    long = serializers.FloatField(write_only=True)
    lat = serializers.FloatField(write_only=True)

    class Meta(BasePositionSerializer.Meta):
        exclude = None
        fields = ["long", "lat"]
