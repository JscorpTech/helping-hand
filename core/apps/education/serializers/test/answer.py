from rest_framework import serializers

from ...models import AnswerModel


class BaseAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerModel
        exclude = [
            "created_at",
            "updated_at",
        ]


class ListAnswerSerializer(BaseAnswerSerializer):
    class Meta(BaseAnswerSerializer.Meta): ...


class RetrieveAnswerSerializer(BaseAnswerSerializer):
    class Meta(BaseAnswerSerializer.Meta): ...


class CreateAnswerSerializer(BaseAnswerSerializer):
    class Meta(BaseAnswerSerializer.Meta): ...
