from rest_framework import serializers

from ...models import GroupModel
from django.contrib.auth import get_user_model


class BaseGroupSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_new_message_count(self, obj):
        try:
            return obj.messages.filter(is_read=False).count()
        except Exception:
            return 0

    def get_user(self, obj):
        from ..user import ListUserSerializer

        obj = obj.get_user(self.context["request"].user, obj)
        if obj is None:
            return None
        return ListUserSerializer(obj, context=self.context).data

    def get_name(self, obj):
        try:
            return obj.chat_name(self.context["request"].user, obj)
        except:
            return None

    def get_image(self, obj):
        return obj.chat_image(self.context["request"].user, obj, self.context["request"])

    def get_last_message(self, obj):
        from .message import ListMessageSerializer

        try:
            messages = obj.messages
            if messages.exists():
                return ListMessageSerializer(messages.last()).data
            return None
        except Exception:
            return None

    class Meta:
        model = GroupModel
        exclude = [
            "created_at",
            "updated_at",
            "users",
        ]
        extra_kwargs = {
            "name": {"read_only": True},
        }


class WsGroupSerializer(BaseGroupSerializer):
    class Meta(BaseGroupSerializer.Meta):
        exclude = None
        fields = [
            "id",
            "name",
            "chat_type",
        ]


class ListGroupSerializer(BaseGroupSerializer):
    image = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    new_message_count = serializers.SerializerMethodField()

    class Meta(BaseGroupSerializer.Meta): ...


class RetrieveGroupSerializer(BaseGroupSerializer):
    user = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    new_message_count = serializers.SerializerMethodField()

    class Meta(BaseGroupSerializer.Meta): ...


class CreateGroupSerializer(BaseGroupSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
    )
    image = serializers.ImageField(required=False)

    class Meta(BaseGroupSerializer.Meta):
        exclude = None
        fields = ["user", "image"]
