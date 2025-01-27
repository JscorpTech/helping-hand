from rest_framework import serializers
from django.contrib.auth import get_user_model
from ...models import NotificationModel, UserNotificationModel
from core.apps.shared.serializers import AbstractTranslatedSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id"]


class BaseNotificationSerializer(AbstractTranslatedSerializer):
    class Meta:
        model = NotificationModel
        fields = ["id", "title", "body", "users", "created_at", "updated_at"]
        translated_fields = ["title", "body"]
        translated = 1


class CreateNotificationSerializer(BaseNotificationSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=get_user_model().objects.all(), required=False)

    def create(self, validated_data):
        users = validated_data.get("users")
        if users == "all":
            validated_data.pop("users")
            instance = NotificationModel.objects.create(**validated_data)
            instance.users.set(get_user_model().objects.all())
            return instance
        return super().create(validated_data)

    class Meta(BaseNotificationSerializer.Meta):
        fields = ["id", "title", "body", "users", "created_at", "updated_at"]


class ListNotificationSerializer(BaseNotificationSerializer):
    class Meta(BaseNotificationSerializer.Meta): ...


class RetrieveNotificationSerializer(BaseNotificationSerializer):
    class Meta(BaseNotificationSerializer.Meta): ...


# ///


class NotificationSerializer(AbstractTranslatedSerializer):
    class Meta:
        model = NotificationModel
        fields = ["id", "title", "body", "created_at", "updated_at"]
        translated_fields = ["title", "body"]
        translated = 1


class UserNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer(read_only=True)

    class Meta:
        model = UserNotificationModel
        fields = ["notification", "is_read", "read_at", "created_at", "updated_at"]
