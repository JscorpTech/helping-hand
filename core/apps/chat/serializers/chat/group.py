from rest_framework import serializers

from ...models import GroupModel
from django.contrib.auth import get_user_model


class BaseGroupSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.chat_name(self.context["request"].user, obj)

    def get_last_message(self, obj):
        from .message import ListMessageSerializer

        try:
            return ListMessageSerializer(obj.messages.last()).data
        except Exception:
            return None

    class Meta:
        model = GroupModel
        exclude = [
            "created_at",
            "updated_at",
            "users",
        ]


class WsGroupSerializer(BaseGroupSerializer):
    class Meta(BaseGroupSerializer.Meta):
        exclude = None
        fields = [
            "id",
            "name",
            "chat_type",
        ]


class ListGroupSerializer(BaseGroupSerializer):
    class Meta(BaseGroupSerializer.Meta): ...


class RetrieveGroupSerializer(BaseGroupSerializer):
    class Meta(BaseGroupSerializer.Meta): ...


class CreateGroupSerializer(BaseGroupSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
    )

    class Meta(BaseGroupSerializer.Meta):
        exclude = None
        fields = [
            "user",
        ]
