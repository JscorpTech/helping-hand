from rest_framework import serializers

from ...models import MessageModel
from ..user import ListUserSerializer
from .group import WsGroupSerializer
from core.apps.shared.serializers import FileSerializer
from typing import Union


class BaseMessageSerializer(serializers.ModelSerializer):
    user = ListUserSerializer()

    def get_file(self, obj) -> Union[FileSerializer, None]:
        if obj.file:
            return FileSerializer(obj.file, context=self.context).data
        return None

    class Meta:
        model = MessageModel
        exclude = []


class ListMessageSerializer(BaseMessageSerializer):
    file = serializers.SerializerMethodField()

    class Meta(BaseMessageSerializer.Meta):
        exclude = BaseMessageSerializer.Meta.exclude + [
            "group",
        ]


class WsMessageSerializer(BaseMessageSerializer):
    file = serializers.SerializerMethodField()
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
    file = serializers.SerializerMethodField()
    class Meta(BaseMessageSerializer.Meta): ...


class CreateMessageSerializer(BaseMessageSerializer):
    class Meta(BaseMessageSerializer.Meta):
        exclude = None
        fields = [
            "text",
            "file",
            "file_type",
        ]
