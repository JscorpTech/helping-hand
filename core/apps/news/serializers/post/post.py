from core.apps.shared.serializers import AbstractTranslatedSerializer

from ...models import PostModel


class BasePostSerializer(AbstractTranslatedSerializer):
    class Meta:
        translated_fields = [
            "title",
            "content",
        ]
        translated = 0
        model = PostModel
        fields = ["id", "title", "content", "image", "views", "news_type", "is_top", "created_at"]


class ListPostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        fields = ["id", "title", "image", "views", "news_type", "is_top", "created_at"]


class RetrievePostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta): ...


class CreatePostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        fields = [
            "image",
            "news_type",
            "is_top",
        ]

