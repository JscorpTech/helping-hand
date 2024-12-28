from core.utils import FileUtils
from rest_framework import serializers


class FileSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    extension = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj) -> str:
        try:
            return obj.file.name.split("/")[-1]
        except Exception:
            return None

    def get_url(self, obj) -> str:
        try:
            return self.context["request"].build_absolute_uri(obj.url)
        except Exception:
            return None

    def get_size(self, obj) -> str:
        try:
            return FileUtils.get_file_size(obj.size)
        except Exception:
            return None

    def get_extension(self, obj) -> str:
        try:
            return FileUtils.get_extension(obj.name)
        except Exception:
            return None
