from rest_framework import serializers

from ...models import MessageModel
from ..user import ListUserSerializer


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


class RetrieveMessageSerializer(BaseMessageSerializer):
    class Meta(BaseMessageSerializer.Meta): ...


class CreateMessageSerializer(BaseMessageSerializer):
    class Meta(BaseMessageSerializer.Meta):
        exclude = None
        fields = ["text", "file"]
