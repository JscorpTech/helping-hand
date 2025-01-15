from rest_framework import serializers

from ...models import PostModel
from core.apps.shared.serializers import AbstractTranslatedSerializer


class BasePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ["id", "title", "content", "image", "views", "news_type", "is_top", "created_at"]


class ListPostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        fields = ["id", "title", "image", "views", "news_type", "is_top", "created_at"]


class RetrievePostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta): ...


class CreatePostSerializer(AbstractTranslatedSerializer, BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        fields = [
            "image",
            "news_type",
            "is_top",
        ]
        translated_fields = [
            "title",
            "content",
        ]
