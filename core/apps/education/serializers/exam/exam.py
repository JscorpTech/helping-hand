from rest_framework import serializers

from ...models import ExamModel
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
    class Meta(BaseExamSerializer.Meta): ...


class CreateExamSerializer(BaseExamSerializer):
    class Meta(BaseExamSerializer.Meta): ...
