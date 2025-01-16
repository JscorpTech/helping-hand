from rest_framework import serializers

from ...models import TestModel, QuestionModel, VariantModel
from ...serializers.test.question import ListQuestionSerializer, CreateQuestionSerializer
from django.db import transaction
from core.apps.shared.serializers import AbstractTranslatedSerializer


class BaseTestSerializer(AbstractTranslatedSerializer):
    questions = ListQuestionSerializer(many=True)
    questions_count = serializers.SerializerMethodField()

    def get_questions_count(self, obj) -> int:
        return obj.questions.count()

    class Meta:
        model = TestModel
        fields = [
            "id",
            "questions_count",
            "questions",
            "topic",
            "desc",
            "time",
        ]


class ListTestSerializer(BaseTestSerializer):
    class Meta(BaseTestSerializer.Meta): ...


class RetrieveTestSerializer(BaseTestSerializer):
    class Meta(BaseTestSerializer.Meta): ...


class CreateTestSerializer(BaseTestSerializer):
    questions = CreateQuestionSerializer(many=True)

    def create(self, validated_data):
        tutorial = self.context["tutorial"]
        questions = validated_data.pop("questions")
        with transaction.atomic():
            test = TestModel.objects.create(**validated_data)
            for question in questions:
                question["test"] = test
                variants = question.pop("variants")
                question = QuestionModel.objects.create(**question)
                for variant in variants:
                    variant["question"] = question
                    VariantModel.objects.create(**variant)
            tutorial.test = test
            tutorial.save()
        return test

    class Meta(BaseTestSerializer.Meta):
        translated_fields = [
            "topic",
            "desc",
        ]
        translated = 2
        fields = [
            "id",
            "time",
            "topic",
            "desc",
            "questions",
        ]
