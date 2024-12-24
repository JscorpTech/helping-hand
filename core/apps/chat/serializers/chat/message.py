from rest_framework import serializers

from ...models import MessageModel
from ..user import ListUserSerializer
from .group import WsGroupSerializer


class BaseMessageSerializer(serializers.ModelSerializer):
    user = ListUserSerializer()

    class Meta:
        model = MessageModel
        exclude = [
            "created_at",
            "updated_at",
        ]


class ListMessageSerializer(BaseMessageSerializer):
    class Meta(BaseMessageSerializer.Meta):
        exclude = BaseMessageSerializer.Meta.exclude + [
            "group",
        ]


class WsMessageSerializer(BaseMessageSerializer):
    group = WsGroupSerializer()

    class Meta(BaseMessageSerializer.Meta):
        exclude = None
        fields = [
            "id",
            "text",
            "file",
            "file_type",
            "user",
            "group",
            "created_at",
        ]


class RetrieveMessageSerializer(BaseMessageSerializer):
    class Meta(BaseMessageSerializer.Meta): ...


class CreateMessageSerializer(BaseMessageSerializer):
    class Meta(BaseMessageSerializer.Meta):
        exclude = None
        fields = [
            "text",
            "file",
            "file_type",
        ]
