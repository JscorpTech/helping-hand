from typing import Any

from rest_framework import serializers

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


class CsListFaqCategorySerializer(AbstractTranslatedSerializer):
    class Meta:
        model = FaqCategoryModel
        fields = ["id", "name"]
        translated_fields = ["name"]
        translated = 0


# ///
class BaseFaqSerializer(AbstractTranslatedSerializer):
    class Meta:
        model = FaqModel
        fields = ["id", "question", "answer", "category", "updated_at", "created_at"]
        translated_fields = ["question", "answer"]
        translated = 1


class ListFaqSerializer(AbstractTranslatedSerializer):
    category = CsListFaqCategorySerializer()

    class Meta:
        model = FaqModel
        fields = ["id", "question", "answer", "category", "updated_at", "created_at"]
        translated_fields = ["question", "answer"]
        translated = 1


class RetreiveFaqSerializer(AbstractTranslatedSerializer):
    category = CsListFaqCategorySerializer()

    class Meta:
        model = FaqModel
        fields = ["id", "question", "answer", "category", "updated_at", "created_at"]
        translated_fields = ["question", "answer"]
        translated = 1


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
