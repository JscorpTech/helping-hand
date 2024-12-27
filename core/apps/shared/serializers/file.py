from core.utils import FileUtils
from rest_framework import serializers


class FileSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    extension = serializers.SerializerMethodField()

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.url)

    def get_size(self, obj):
        return FileUtils.get_file_size(obj.size)

    def get_extension(self, obj):
        return FileUtils.get_extension(obj.name)
