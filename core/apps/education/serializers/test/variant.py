from rest_framework import serializers

from ...models import VariantModel


class BaseVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantModel
        exclude = ["created_at", "updated_at", "question", "is_true"]


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
            "variant",
            "bal",
        ]
