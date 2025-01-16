from rest_framework import serializers

from ...models import TaskModel
from core.apps.shared.serializers import FileSerializer, AbstractTranslatedSerializer


class BaseTaskSerializer(AbstractTranslatedSerializer):
    class Meta:
        model = TaskModel
        translated_fields = [
            "name",
            "desc",
        ]
        exclude = [
            "created_at",
            "updated_at",
        ]


class ListTaskSerializer(BaseTaskSerializer):
    class Meta(BaseTaskSerializer.Meta): ...


class RetrieveTaskSerializer(BaseTaskSerializer):
    file = FileSerializer()

    class Meta(BaseTaskSerializer.Meta): ...


class CreateTaskSerializer(BaseTaskSerializer):
    class Meta(BaseTaskSerializer.Meta):
        translated = 2


class TaskAnswerSerializer(serializers.Serializer):
    answer = serializers.CharField(required=False)
    file = serializers.FileField(required=False)
