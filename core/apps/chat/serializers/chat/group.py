from rest_framework import serializers

from ...models import GroupModel
from django.contrib.auth import get_user_model


class BaseGroupSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_new_message_count(self, obj) -> int:
        if not self.context["request"].user.is_authenticated:
            return 0
        return obj.new_message_count(self.context["request"].user)

    def get_user(self, obj):
        from ..user import ListUserSerializer

        user = self.context["request"].user
        if not user.is_authenticated:
            return None
        obj = obj.get_chat_details(user)
        if obj["type"] == "group":
            return None
        return ListUserSerializer(get_user_model().objects.get(id=obj["id"]), context=self.context).data

    def get_name(self, obj):
        if not self.context["request"].user.is_authenticated:
            return obj.name
        return obj.get_chat_details(self.context["request"].user)["name"]

    def get_image(self, obj):
        try:
            if not self.context["request"].user.is_authenticated:
                return self.context["request"].build_absolute_uri(obj.image.url)
            return obj.chat_image(self.context["request"].user, self.context["request"])
        except Exception:
            return None

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


class CreatePublicGroupSerializer(BaseGroupSerializer):
    name = None

    class Meta(BaseGroupSerializer.Meta):
        exclude = None
        fields = [
            "name",
            "image",
            "chat_type",
        ]
        extra_kwargs = {
            "name": {"required": True},
            "image": {"required": True},
            "chat_type": {"required": True},
        }


class CreateGroupSerializer(BaseGroupSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
    )
    image = serializers.ImageField(required=False)

    class Meta(BaseGroupSerializer.Meta):
        exclude = None
        fields = ["user", "image"]
