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
            "created_at",
            "updated_at"
        ]


class ListPostSerializer(BasePostSerializer):
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        return "%s" % obj.content[:100]

    class Meta(BasePostSerializer.Meta): ...


class RetrievePostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta): ...


class CreatePostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta): ...
