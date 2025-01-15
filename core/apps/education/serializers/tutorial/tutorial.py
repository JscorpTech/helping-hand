from rest_framework import serializers

from ...models import TutorialModel, ResultModel, TaskResultModel
from core.apps.shared.serializers import AbstractTranslatedSerializer


class BaseTutorialSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    test_count = serializers.SerializerMethodField()

    def get_test_count(self, obj) -> int:
        return obj.test.questions.count() if obj.test else 0

    def get_is_completed(self, obj) -> bool:
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return (
                    ResultModel.objects.filter(user=user, tutorial=obj).exists()
                    and TaskResultModel.objects.filter(user=user, tutorial=obj).exists()
                )
        return False

    class Meta:
        model = TutorialModel
        fields = [
            "id",
            "name",
            "desc",
            "image",
            "file",
            "video",
            "tags",
            "position",
            "source",
            "test_count",
            "updated_at"
        ]


class ListTutorialSerializer(BaseTutorialSerializer):
    desc = serializers.SerializerMethodField()

    def get_desc(self, obj):
        return obj.desc[:200] if obj.desc else ""

    class Meta(BaseTutorialSerializer.Meta): ...


class ScoreSerializer(serializers.Serializer):
    success = serializers.IntegerField()
    total = serializers.IntegerField()
    passed = serializers.BooleanField(default=False)


class RetrieveTutorialSerializer(BaseTutorialSerializer):
    test_score = serializers.SerializerMethodField()
    task_passed = serializers.SerializerMethodField()

    def get_task_passed(self, obj) -> bool:
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return TaskResultModel.objects.filter(tutorial=obj, user=user).exists()
        return False

    def get_test_score(self, obj) -> ScoreSerializer:
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                result = ResultModel.objects.filter(tutorial=obj, user=user).first()
                if result:
                    return ScoreSerializer({"success": result.score, "total": result.total, "passed": True}).data
        return ScoreSerializer({"success": 0, "total": 0}).data

    class Meta(BaseTutorialSerializer.Meta):
        fields = BaseTutorialSerializer.Meta.fields + [
            "test_score",
            "task_passed",
        ]


class CreateTutorialSerializer(AbstractTranslatedSerializer, BaseTutorialSerializer):

    class Meta(BaseTutorialSerializer.Meta):
        exclude = None
        translated_fields = [
            "name",
            "desc",
        ]
        fields = [
            "id",
            "image",
            "file",
            "video",
            "test",
            "tags",
            "position",
            "source",
        ]
