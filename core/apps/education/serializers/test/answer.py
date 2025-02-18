from rest_framework import serializers

from ...models import QuestionModel, VariantModel


class CreateAnswerSerializer(serializers.Serializer):
    any = serializers.CharField(required=False)
    question = serializers.PrimaryKeyRelatedField(queryset=QuestionModel.objects.all())
    variant = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=VariantModel.objects.all()))

    class Meta:
        fields = [
            "question",
            "variant",
            "any",
        ]


class AnswerSerializer(serializers.ListSerializer):
    child = CreateAnswerSerializer()
