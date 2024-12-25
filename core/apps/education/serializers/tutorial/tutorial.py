from rest_framework import serializers

from ...models import TutorialModel


class BaseTutorialSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    def get_is_completed(self, obj) -> bool:
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return obj.users.filter(id=user.id).exists()
        return False

    class Meta:
        model = TutorialModel
        exclude = ["created_at", "updated_at", "test", "users"]


class ListTutorialSerializer(BaseTutorialSerializer):
    desc = serializers.SerializerMethodField()

    def get_desc(self, obj):
        return obj.desc[:200]

    class Meta(BaseTutorialSerializer.Meta): ...


class RetrieveTutorialSerializer(BaseTutorialSerializer):
    class Meta(BaseTutorialSerializer.Meta): ...


class CreateTutorialSerializer(BaseTutorialSerializer):
    class Meta(BaseTutorialSerializer.Meta):
        exclude = None
        fields = [
            "id",
            "name",
            "desc",
            "image",
            "file",
            "video",
            "test",
            "tags",
            "position",
            "source",
        ]
