from ...models import VariantModel
from core.apps.shared.serializers import AbstractTranslatedSerializer


class BaseVariantSerializer(AbstractTranslatedSerializer):
    class Meta:
        translated_fields = [
            "variant",
        ]
        model = VariantModel
        fields = [
            "id",
            "bal",
            "variant"
        ]


class ListVariantSerializer(BaseVariantSerializer):
    class Meta(BaseVariantSerializer.Meta): ...


class RetrieveVariantSerializer(BaseVariantSerializer):
    class Meta(BaseVariantSerializer.Meta): ...


class CreateVariantSerializer(BaseVariantSerializer):
    class Meta(BaseVariantSerializer.Meta):
        exclude = None
        fields = [
            "id",
            "is_true",
            "bal",
        ]
        translated = 2
