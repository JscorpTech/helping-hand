from ...models import QuestionModel, VariantModel
from ..test.variant import ListVariantSerializer, CreateVariantSerializer
from core.apps.shared.serializers import AbstractTranslatedSerializer
from django.utils.html import strip_tags


class BaseQuestionSerializer(AbstractTranslatedSerializer):
    variants = ListVariantSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["question"] = strip_tags(data["question"])
        return data

    class Meta:
        model = QuestionModel
        translated_fields = [
            "question",
        ]
        fields = [
            "id",
            "is_any",
            "is_many",
            "variants",
            "question",
        ]


class ListQuestionSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta): ...


class RetrieveQuestionSerializer(BaseQuestionSerializer):
    class Meta(BaseQuestionSerializer.Meta): ...


class CreateQuestionSerializer(BaseQuestionSerializer):
    variants = CreateVariantSerializer(many=True, required=True)

    def update(self, instance, validated_data):
        variants = validated_data.pop("variants")
        question = super().update(instance, validated_data)
        instance.variants.all().delete()
        for variant in variants:
            variant["question"] = question
            VariantModel.objects.create(**variant)
        return question

    class Meta(BaseQuestionSerializer.Meta):
        fields = BaseQuestionSerializer.Meta.fields + ["variants"]
        translated = 2
        fields = [
            "id",
            "is_any",
            "is_many",
            "variants",
            "question",
        ]
