from rest_framework import serializers

from ...models import TestModel
from ...serializers.test.question import ListQuestionSerializer


class BaseTestSerializer(serializers.ModelSerializer):
    questions = ListQuestionSerializer(many=True)
    questions_count = serializers.SerializerMethodField()

    def get_questions_count(self, obj) -> int:
        return obj.questions.count()

    class Meta:
        model = TestModel
        exclude = [
            "created_at",
            "updated_at",
        ]


class ListTestSerializer(BaseTestSerializer):
    class Meta(BaseTestSerializer.Meta): ...


class RetrieveTestSerializer(BaseTestSerializer):
    class Meta(BaseTestSerializer.Meta): ...


class CreateTestSerializer(BaseTestSerializer):
    class Meta(BaseTestSerializer.Meta): ...
