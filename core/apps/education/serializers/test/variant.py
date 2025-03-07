from core.apps.shared.serializers import AbstractTranslatedSerializer

from ...models import VariantModel


class BaseVariantSerializer(AbstractTranslatedSerializer):
    class Meta:
        translated_fields = [
            "variant",
        ]
        model = VariantModel
        fields = ["id", "bal", "variant"]


class ListVariantSerializer(BaseVariantSerializer):
    class Meta(BaseVariantSerializer.Meta):
        exclude = None
        fields = ["id", "is_true", "bal", "variant"]


class RetrieveVariantSerializer(BaseVariantSerializer):
    class Meta(BaseVariantSerializer.Meta): ...


class CreateVariantSerializer(BaseVariantSerializer):
    class Meta(BaseVariantSerializer.Meta):
        exclude = None
        fields = ["id", "is_true", "bal", "variant"]
        translated = 2
