from django.conf import settings
from rest_framework import serializers


class AbstractTranslatedSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field in self.Meta.translated_fields:
            for lang, _ in settings.LANGUAGES:
                translated_field = f"{field}_{lang}"
                representation[translated_field] = getattr(instance, translated_field)
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        for field in self.Meta.translated_fields:
            for lang, _ in settings.LANGUAGES:
                translated_field = f"{field}_{lang}"
                if translated_field in data:
                    internal_value[translated_field] = data[translated_field]
        return internal_value
