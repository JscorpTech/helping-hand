from rest_framework import serializers

from ...models import TaskModel


class BaseTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        exclude = [
            "created_at",
            "updated_at",
        ]


class ListTaskSerializer(BaseTaskSerializer):
    class Meta(BaseTaskSerializer.Meta): ...


class RetrieveTaskSerializer(BaseTaskSerializer):
    class Meta(BaseTaskSerializer.Meta): ...


class CreateTaskSerializer(BaseTaskSerializer):
    class Meta(BaseTaskSerializer.Meta): ...


class TaskAnswerSerializer(serializers.Serializer):
    answer = serializers.CharField(required=False)
    file = serializers.FileField(required=False)
