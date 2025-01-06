from rest_framework import serializers

from ...models import PostModel


class BasePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = [
            "id",
            "title",
            "content",
            "image",
            "views",
            "created_at"
        ]


class ListPostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        fields = [
            "id",
            "title",
            "image",
            "views",
            "created_at"
        ]


class RetrievePostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta): ...


class CreatePostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta): ...
