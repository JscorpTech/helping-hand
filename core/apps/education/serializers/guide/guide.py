from rest_framework import serializers

from ...models import GuideModel


class BaseGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideModel
        exclude = [
            "created_at",
            "updated_at",
        ]


class ListGuideSerializer(BaseGuideSerializer):
    class Meta(BaseGuideSerializer.Meta): ...


class RetrieveGuideSerializer(BaseGuideSerializer):
    class Meta(BaseGuideSerializer.Meta): ...


class CreateGuideSerializer(BaseGuideSerializer):
    class Meta(BaseGuideSerializer.Meta): ...
