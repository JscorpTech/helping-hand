from rest_framework import serializers
from ...choices import ProgressChoices


class BaseProgressSerializer(serializers.Serializer): ...


class ListProgressSerializer(BaseProgressSerializer):
    name = serializers.CharField()
    status = serializers.ChoiceField(choices=ProgressChoices.choices)
