from rest_framework import serializers

from ...models import UserRequestModel


class BaseUserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequestModel
        exclude = [
            "created_at",
            "updated_at",
        ]


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
