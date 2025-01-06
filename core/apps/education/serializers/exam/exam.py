from rest_framework import serializers

from ...models import ExamModel, ExamResultModel
from ..test import RetrieveTestSerializer


class BaseExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamModel
        exclude = [
            "created_at",
            "updated_at",
        ]


class ListExamSerializer(BaseExamSerializer):
    class Meta(BaseExamSerializer.Meta): ...


class RetrieveExamSerializer(BaseExamSerializer):
    test = RetrieveTestSerializer()
    is_passed = serializers.SerializerMethodField()

    def get_is_passed(self, obj) -> bool:
        return ExamResultModel.objects.filter(user=self.context["request"].user, exam=obj).exists()

    class Meta(BaseExamSerializer.Meta): ...


class CreateExamSerializer(BaseExamSerializer):
    class Meta(BaseExamSerializer.Meta): ...
