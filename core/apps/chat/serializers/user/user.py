from django.contrib.auth import get_user_model
from rest_framework import serializers


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "role"
        ]


class ListUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta): ...


class RetrieveUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta): ...


class CreateUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta): ...
