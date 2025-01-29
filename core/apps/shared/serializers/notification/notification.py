from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...models import NotificationModel, UserNotificationModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id"]


class BaseNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationModel
        fields = ["id", "title", "body", "users", "created_at", "updated_at"]


class CreateNotificationSerializer(BaseNotificationSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=get_user_model().objects.all(), required=False)
    is_all_users = serializers.BooleanField(default=False, required=False, write_only=True)

    def create(self, validated_data):
        users = validated_data.pop("users", None)
        is_all_users = validated_data.pop("is_all_users", False)
        instance = NotificationModel.objects.create(**validated_data)
        if is_all_users:
            instance.users.set(get_user_model().objects.all())
        elif users:
            instance.users.set(users)
        return instance

    class Meta(BaseNotificationSerializer.Meta):
        fields = ["id", "title", "body", "users", "is_all_users", "created_at", "updated_at"]


class ListNotificationSerializer(BaseNotificationSerializer):
    class Meta(BaseNotificationSerializer.Meta): ...


class RetrieveNotificationSerializer(BaseNotificationSerializer):
    class Meta(BaseNotificationSerializer.Meta): ...


# ///


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationModel
        fields = ["id", "title", "body", "created_at", "updated_at"]


class UserNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer(read_only=True)

    class Meta:
        model = UserNotificationModel
        fields = ["notification", "is_read", "read_at", "created_at", "updated_at"]
