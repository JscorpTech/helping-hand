from rest_framework import serializers

from ...models import GuideModel
from core.apps.shared.serializers import FileSerializer


class BaseGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideModel
        exclude = [
            "created_at",
            "updated_at",
        ]


class ListGuideSerializer(BaseGuideSerializer):
    desc = serializers.SerializerMethodField()
    file = FileSerializer()

    def get_desc(self, obj):
        return "%s..." % obj.desc[:200]

    class Meta(BaseGuideSerializer.Meta): ...


class RetrieveGuideSerializer(BaseGuideSerializer):
    file = FileSerializer()

    class Meta(BaseGuideSerializer.Meta): ...


class CreateGuideSerializer(BaseGuideSerializer):
    class Meta(BaseGuideSerializer.Meta): ...
