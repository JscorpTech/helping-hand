from rest_framework import serializers

from ...models import TutorialModel


class BaseTutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialModel
        exclude = [
            "created_at",
            "updated_at",
            "test",
        ]


class ListTutorialSerializer(BaseTutorialSerializer):
    desc = serializers.SerializerMethodField()

    def get_desc(self, obj):
        return obj.desc[:200]

    class Meta(BaseTutorialSerializer.Meta): ...


class RetrieveTutorialSerializer(BaseTutorialSerializer):
    class Meta(BaseTutorialSerializer.Meta): ...


class CreateTutorialSerializer(BaseTutorialSerializer):
    class Meta(BaseTutorialSerializer.Meta): ...
