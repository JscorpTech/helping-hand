from rest_framework import serializers

from ...models import MessageModel
from ..user import ListUserSerializer
from .group import WsGroupSerializer
from core.apps.shared.serializers import FileSerializer


class BaseMessageSerializer(serializers.ModelSerializer):
    user = ListUserSerializer()

    class Meta:
        model = MessageModel
        exclude = []


class ListMessageSerializer(BaseMessageSerializer):
    file = FileSerializer()

    class Meta(BaseMessageSerializer.Meta):
        exclude = BaseMessageSerializer.Meta.exclude + [
            "group",
        ]


class WsMessageSerializer(BaseMessageSerializer):
    file = FileSerializer()
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
    file = FileSerializer()
    class Meta(BaseMessageSerializer.Meta): ...


class CreateMessageSerializer(BaseMessageSerializer):
    class Meta(BaseMessageSerializer.Meta):
        exclude = None
        fields = [
            "text",
            "file",
            "file_type",
        ]
