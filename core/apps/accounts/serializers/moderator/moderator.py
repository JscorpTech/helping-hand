from rest_framework import serializers

from ...models import ModeratorModel
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from datetime import datetime
from ...choices import RoleChoice


class BaseModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeratorModel
        exclude = [
            "created_at",
            "updated_at",
        ]


class ListModeratorSerializer(BaseModeratorSerializer):
    class Meta(BaseModeratorSerializer.Meta): ...


class RetrieveModeratorSerializer(BaseModeratorSerializer):
    class Meta(BaseModeratorSerializer.Meta): ...


class CreateModeratorSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    level = serializers.CharField(max_length=255)
    experience = serializers.CharField(max_length=255)
    role = serializers.ChoiceField(choices=RoleChoice.choices)

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            phone=validated_data["phone"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            validated_at=datetime.now(),
            role=validated_data["role"],
        )
        ModeratorModel.objects.create(
            experience=validated_data["experience"], level=validated_data["level"], user=user
        )
        return user

    def update(self, instance, validated_data):
        user = instance
        user.first_name = validated_data.get("first_name", user.first_name)
        user.last_name = validated_data.get("last_name", user.last_name)
        user.role = validated_data.get("role", user.role)
        user.phone = validated_data.get("phone", user.phone)
        if "password" in validated_data:
            user.set_password(validated_data["password"])
        user.save()
        if not hasattr(instance, "moderator"):
            return instance
        moderator = instance.moderator
        moderator.experience = validated_data.get("experience", moderator.experience)
        moderator.level = validated_data.get("level", moderator.level)
        moderator.save()
        return instance

    def validate_phone(self, value):
        if self.instance and self.instance.phone == value:
            return value
        user = get_user_model().objects.filter(phone=value)
        if user.exists():
            raise ValidationError(_("Phone number already registered."))
        return value
