from core.utils import FileUtils
from rest_framework import serializers


class FileSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    extension = serializers.SerializerMethodField()

    def get_url(self, obj):
        try:
            return self.context["request"].build_absolute_uri(obj.url)
        except Exception:
            return None

    def get_size(self, obj):
        try:
            return FileUtils.get_file_size(obj.size)
        except Exception:
            return None

    def get_extension(self, obj):
        try:
            return FileUtils.get_extension(obj.name)
        except Exception:
            return None
