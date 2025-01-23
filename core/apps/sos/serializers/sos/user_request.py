from rest_framework import serializers

from ...models import UserRequestModel
from core.apps.accounts.serializers import UserSerializer


class BaseUserRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserRequestModel
        exclude = []


class ListUserRequestSerializer(BaseUserRequestSerializer):
    class Meta(BaseUserRequestSerializer.Meta): ...


class RetrieveUserRequestSerializer(BaseUserRequestSerializer):
    class Meta(BaseUserRequestSerializer.Meta): ...


class CreateUserRequestSerializer(BaseUserRequestSerializer):
    class Meta(BaseUserRequestSerializer.Meta):
        exclude = None
        fields = [
            "area",
        ]
