from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..choices import RoleChoice


class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["role"] in RoleChoice.moderator_roles():
            if instance.moderator:
                data["level"] = instance.moderator.level
                data["experience"] = instance.moderator.experience
            else:
                data["level"] = None
                data["experience"] = None
        return data

    class Meta:
        exclude = [
            "created_at",
            "updated_at",
            "password",
            "groups",
            "user_permissions",
        ]
        model = get_user_model()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "avatar",
            "bio",
        ]
