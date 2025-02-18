from ...models import BannerModel
from ..base import AbstractTranslatedSerializer


class BaseBannerSerializer(AbstractTranslatedSerializer):
    class Meta:
        model = BannerModel
        translated_fields = ["title", "subtitle"]
        fields = [
            "id",
            "title",
            "subtitle",
            "color_right",
            "color_left",
            "image",
            "link",
        ]


class ListBannerSerializer(BaseBannerSerializer):
    class Meta(BaseBannerSerializer.Meta): ...


class RetrieveBannerSerializer(BaseBannerSerializer):
    class Meta(BaseBannerSerializer.Meta): ...


class CreateBannerSerializer(BaseBannerSerializer):
    class Meta(BaseBannerSerializer.Meta):
        translated = 2
