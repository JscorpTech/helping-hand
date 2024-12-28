from rest_framework import serializers

from ...models import ExamResultModel


class BaseExamresultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResultModel
        exclude = [
            "created_at",
            "updated_at",
        ]


class ListExamresultSerializer(BaseExamresultSerializer):
    class Meta(BaseExamresultSerializer.Meta): ...


class RetrieveExamresultSerializer(BaseExamresultSerializer):
    class Meta(BaseExamresultSerializer.Meta): ...


class CreateExamresultSerializer(BaseExamresultSerializer):
    class Meta(BaseExamresultSerializer.Meta): ...
