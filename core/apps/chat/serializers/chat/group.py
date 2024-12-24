from rest_framework import serializers

from ...models import GroupModel


class BaseGroupSerializer(serializers.ModelSerializer):
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
    class Meta(BaseGroupSerializer.Meta): ...
