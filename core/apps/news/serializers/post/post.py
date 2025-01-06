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
            "news_type",
            "created_at"
        ]


class ListPostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        fields = [
            "id",
            "title",
            "image",
            "views",
            "news_type",
            "created_at"
        ]


class RetrievePostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta): ...


class CreatePostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta): ...
