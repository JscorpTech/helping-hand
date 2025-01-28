from rest_framework import serializers
from typing import Any
from core.apps.shared.serializers import AbstractTranslatedSerializer
from ...models import FaqCategoryModel, FaqModel


class BaseFaqCategorySerializer(AbstractTranslatedSerializer):
    class Meta:
        model = FaqCategoryModel
        fields = ["id", "name", "updated_date", "created_date"]
        translated_fields = ["name"]
        translated = 1


class ListFaqCategorySerializer(BaseFaqCategorySerializer):
    class Meta(BaseFaqCategorySerializer.Meta): ...


class RetreiveFaqCategorySerializer(BaseFaqCategorySerializer):
    class Meta(BaseFaqCategorySerializer.Meta): ...


class CreateFaqCategorySerializer(BaseFaqCategorySerializer):
    class Meta(BaseFaqCategorySerializer.Meta): ...


class CsListFaqCategorySerializer(AbstractTranslatedSerializer):
    class Meta:
        model = FaqCategoryModel
        fields = ["id", "name"]
        translated_fields = ["name"]
        translated = 1


# ///
class BaseFaqSerializer(AbstractTranslatedSerializer):
    class Meta:
        model = FaqModel
        fields = ["id", "question", "answer", "updated_date", "category", "created_date"]
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
