from rest_framework import serializers
from typing import Any
from core.apps.shared.serializers import AbstractTranslatedSerializer
from ...models import FaqCategoryModel, FaqModel


class BaseFaqCategorySerializer(AbstractTranslatedSerializer):
    class Meta:
        model = FaqCategoryModel
        fields = ["id", "name", "updated_at", "created_at"]
        translated_fields = ["name"]
        translated = 1


class ListFaqCategorySerializer(BaseFaqCategorySerializer):
    class Meta(BaseFaqCategorySerializer.Meta): ...


class RetreiveFaqCategorySerializer(BaseFaqCategorySerializer):
    class Meta(BaseFaqCategorySerializer.Meta): ...


class CreateFaqCategorySerializer(BaseFaqCategorySerializer):
    class Meta(BaseFaqCategorySerializer.Meta): ...


# ///
class BaseFaqSerializer(AbstractTranslatedSerializer):
    class Meta:
        model = FaqModel
        fields = ["id", "question", "answer", "category", "updated_at", "created_at"]
        translated_fields = ["question", "answer"]
        translated = 1


class ListFaqSerializer(BaseFaqSerializer):
    class Meta(BaseFaqSerializer.Meta): ...


class RetreiveFaqSerializer(BaseFaqSerializer):
    class Meta(BaseFaqSerializer.Meta): ...


class CreateFaqSerializer(BaseFaqSerializer):
    class Meta(BaseFaqSerializer.Meta): ...


class FaqsSerializer(serializers.ModelSerializer):
    faqs = serializers.SerializerMethodField()

    class Meta:
        model = FaqCategoryModel
        fields = ["id", "name", "faqs"]

    def get_faqs(self, obj) -> Any:
        faqs = FaqModel.objects.filter(category=obj)
        return BaseFaqSerializer(faqs, many=True).data

    def to_representation(self, obj) -> Any:
        rep = super().to_representation(obj)
        rep["faqs"] = self.get_faqs(obj)
        return rep
