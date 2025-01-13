from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.apps.chat.models import GroupModel
from ..choices import RoleChoice
from core.apps.accounts.choices import AuthProviderChoice


class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["role"] in RoleChoice.moderator_roles():
            if hasattr(instance, "moderator"):
                data["level"] = instance.moderator.level
                data["experience"] = instance.moderator.experience
            else:
                data["level"] = None
                data["experience"] = None
            if self.context.get("type") == "moderator" and self.context.get("request").user.is_authenticated:
                chat = GroupModel.objects.filter(users__in=[instance, self.context["request"].user], is_public=False)
                data["chat"] = chat.first().id if chat.exists() else None
            else:
                data["chat"] = None
        if data["auth_provider"] == AuthProviderChoice.GOOGLE:
            data["email"] = data["phone"]
            data["phone"] = None
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
