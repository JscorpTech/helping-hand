from rest_framework import serializers


class CallSerializer(serializers.Serializer):
    ACTIONS = [
        ("call", "call"),
    ]
    group = serializers.IntegerField()
    action = serializers.ChoiceField(choices=ACTIONS)
    data = serializers.JSONField(required=False, default={})
