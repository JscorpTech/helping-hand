from rest_framework import serializers

from core.apps.accounts.serializers import UserSerializer

from ...models import UserRequestModel


class BaseUserRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserRequestModel
        exclude = []


class ListUserRequestSerializer(BaseUserRequestSerializer):
    class Meta(BaseUserRequestSerializer.Meta): ...


class RetrieveUserRequestSerializer(BaseUserRequestSerializer):
    class Meta(BaseUserRequestSerializer.Meta): ...


class TopRequestsSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    user = UserSerializer()


class CreateUserRequestSerializer(BaseUserRequestSerializer):
    class Meta(BaseUserRequestSerializer.Meta):
        exclude = None
        fields = [
            "area",
        ]
