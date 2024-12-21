from rest_framework import serializers

from ...models import QuestionModel
from ..test.variant import ListVariantSerializer


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
    class Meta(BaseQuestionSerializer.Meta): ...
