from ...models import QuestionModel, VariantModel
from ..test.variant import ListVariantSerializer, CreateVariantSerializer
from core.apps.shared.serializers import AbstractTranslatedSerializer
from django.utils.html import strip_tags
from rest_framework.exceptions import ValidationError
from rest_framework import serializers


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
    test_id = serializers.IntegerField(required=False, write_only=True)

    def update(self, instance, validated_data):
        variants = validated_data.pop("variants")
        question = super().update(instance, validated_data)
        instance.variants.all().delete()
        for variant in variants:
            variant["question"] = question
            VariantModel.objects.create(**variant)
        return question

    def create(self, validated_data):
        variants = validated_data.pop("variants")
        question = super().create(validated_data)
        for variant in variants:
            variant["question"] = question
            VariantModel.objects.create(**variant)
        return question

    def validate(self, attrs):
        if "action" in self.context and self.context["action"] == "add_question":
            if not attrs.get("test_id"):
                raise ValidationError({"tes_id": ["test is required"]})
        return attrs

    class Meta(BaseQuestionSerializer.Meta):
        fields = BaseQuestionSerializer.Meta.fields + ["variants"]
        translated = 2
        fields = ["id", "is_any", "is_many", "variants", "question", "test_id"]


class CreateQuestionBulkSerializer(serializers.ListSerializer):
    child = CreateQuestionSerializer()

    def create(self, validated_data):
        serializer = CreateQuestionSerializer(data=validated_data, context={"action": "add_question"}, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    class Meta(BaseQuestionSerializer.Meta):
        fields = BaseQuestionSerializer.Meta.fields + ["variants"]
        translated = 2
