from rest_framework import serializers

from ...models import GuideModel
from core.apps.shared.serializers import FileSerializer
from core.apps.shared.serializers import AbstractTranslatedSerializer


class BaseGuideSerializer(AbstractTranslatedSerializer):
    class Meta:
        model = GuideModel
        translated_fields = ["name", "desc"]
        fields = ["id", "name", "desc", "image", "file", "video", "guide_type", "updated_at"]


class ListGuideSerializer(BaseGuideSerializer):
    desc = serializers.SerializerMethodField()
    file = FileSerializer()

    def get_desc(self, obj) -> str:
        return "%s..." % obj.desc[:200] if obj.desc else None

    class Meta(BaseGuideSerializer.Meta):
        translated_fields = []


class RetrieveGuideSerializer(BaseGuideSerializer):
    file = FileSerializer()

    class Meta(BaseGuideSerializer.Meta):
        fields = BaseGuideSerializer.Meta.fields + ["file"]


class CreateGuideSerializer(BaseGuideSerializer):
    class Meta(BaseGuideSerializer.Meta):
        translated = 2
        fields = [
            "id",
            "image",
            "desc",
            "name",
            "file",
            "video",
            "guide_type",
        ]
