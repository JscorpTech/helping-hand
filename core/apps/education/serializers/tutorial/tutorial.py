from rest_framework import serializers

from ...models import TutorialModel, ResultModel, TaskResultModel


class BaseTutorialSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

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
        exclude = [
            "created_at",
            "updated_at",
            "test",
            "users",
            "task",
        ]


class ListTutorialSerializer(BaseTutorialSerializer):
    desc = serializers.SerializerMethodField()

    def get_desc(self, obj):
        return obj.desc[:200]

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

    class Meta(BaseTutorialSerializer.Meta): ...


class CreateTutorialSerializer(BaseTutorialSerializer):

    class Meta(BaseTutorialSerializer.Meta):
        exclude = None
        fields = [
            "id",
            "name_uz",
            "name_kaa",
            "name_kril",
            "desc_uz",
            "desc_kaa",
            "desc_kril",
            "image",
            "file",
            "video",
            "test",
            "tags",
            "position",
            "source",
        ]
