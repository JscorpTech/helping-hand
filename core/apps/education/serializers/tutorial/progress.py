from rest_framework import serializers
from ...choices import ProgressChoices


class BaseProgressSerializer(serializers.Serializer): ...


class ListProgressSerializer(BaseProgressSerializer):
    id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=ProgressChoices.choices)
