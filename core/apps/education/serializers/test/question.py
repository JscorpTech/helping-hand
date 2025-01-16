from rest_framework import serializers

from ...models import QuestionModel, VariantModel
from ..test.variant import ListVariantSerializer, CreateVariantSerializer


class BaseQuestionSerializer(serializers.ModelSerializer):
    variants = ListVariantSerializer(many=True)

    class Meta:
        model = QuestionModel
        exclude = [
            "created_at",
            "updated_at",
            "test",
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

    class Meta(BaseQuestionSerializer.Meta): ...
