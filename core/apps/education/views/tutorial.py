from typing import Any

from django.utils.translation import gettext as _
from django_core.mixins import BaseViewSetMixin
from django_core.paginations import CustomPagination
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db import transaction

from core.apps.accounts.permissions import IsModeratorPermission

from ..models import AnswerModel, TutorialModel, ResultModel, TaskResultModel
from ..serializers.test import AnswerSerializer, RetrieveTestSerializer
from ..serializers.task import RetrieveTaskSerializer, TaskAnswerSerializer
from ..serializers.tutorial import CreateTutorialSerializer, ListTutorialSerializer, RetrieveTutorialSerializer
from ..services import TestService


@extend_schema(
    tags=["tutorial"],
    parameters=[
        OpenApiParameter(name="search", type=str, description="Search by name, desc, tags"),
    ],
)
class TutorialView(BaseViewSetMixin, ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ["name", "desc", "tags"]

    def get_object(self):
        match self.action:
            case "task" | "task_answer":
                obj = self.get_queryset().get(pk=self.kwargs.get("pk"))
                if obj.task is None:
                    raise NotFound("Task mavjud emas")
                return obj.task
            case _:
                return super().get_object()

    def get_queryset(self):
        match self.action:
            case "test" | "test_answer":
                return (
                    TutorialModel.objects.select_related("test")
                    .prefetch_related("test__questions", "test__questions__variants")
                    .get(pk=self.kwargs.get("pk"))
                    .test
                )
            case "task" | "task_answer":
                return TutorialModel.objects.select_related("task")
            case _:
                return TutorialModel.objects.prefetch_related("users").order_by("position").all()

    def get_serializer_class(self) -> Any:
        match self.action:
            case "list" | "completed":
                return ListTutorialSerializer
            case "retrieve":
                return RetrieveTutorialSerializer
            case "create" | "update" | "partial_update":
                return CreateTutorialSerializer
            case "test":
                return RetrieveTestSerializer
            case "test_answer":
                return AnswerSerializer
            case "task":
                return RetrieveTaskSerializer
            case "task_answer":
                return TaskAnswerSerializer
            case _:
                return ListTutorialSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case "create" | "update" | "partial_update" | "destroy":
                perms.extend([IsAuthenticated, IsModeratorPermission])
            case "completed":
                perms.extend([IsAuthenticated])
            case "test_answer" | "task_answer":
                perms.extend([IsAuthenticated])
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()

    @extend_schema(
        request=AnswerSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string", "example": "Test javoblari qabul qildi"},
                        "success": {"type": "integer", "example": 5},
                        "total": {"type": "integer", "example": 10},
                    },
                }
            )
        },
    )
    @action(methods=["POST"], detail=True, url_path="test-answer", url_name="test-answer")
    def test_answer(self, request, pk=None):
        """Test javoblarini tekshirish"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        test = self.get_queryset()
        questions = test.questions.all()

        if len(data) != len(questions):
            raise ValidationError({"question": [_("Test javoblar soni noto'g'ri.")]})

        success = 0
        bal = 0
        answers = []

        with transaction.atomic():
            for item in data:
                question = item["question"]
                variants = item["variant"]
                TestService.check_answer_validity(question, variants)
                answer, __ = AnswerModel.objects.get_or_create(user=request.user, question=question, tutorial_id=pk)
                answer.variant.set(variants)
                s, b = TestService.calculate_score_and_balance(question, variants)
                success += s
                bal += b

                answers.append(answer)

            TutorialModel.objects.get(pk=pk).users.add(request.user)
            ResultModel.objects.update_or_create(
                user=request.user,
                tutorial_id=pk,
                defaults={"score": success, "total": len(questions), "bal": bal},
            )

            return Response(
                {"detail": _("Test javoblari qabul qilindi."), "success": success, "total": len(questions), "bal": bal}
            )

    @action(methods=["GET"], detail=True, url_path="test", url_name="test")
    def test(self, request, pk=None):
        """Video darsga test"""
        try:
            return Response(self.get_serializer(self.get_queryset()).data)
        except TutorialModel.DoesNotExist:
            raise NotFound(_("Tutorial not found"))

    @extend_schema(
        responses={200: ListTutorialSerializer(many=True)},
    )
    @action(methods=["GET"], detail=False, url_path="completed", url_name="completed")
    def completed(self, request):
        """Yakunlangan video darslar"""
        queryset = self.get_queryset().filter(users__in=[request.user])
        paginator = CustomPagination()
        queryset = paginator.paginate_queryset(queryset, request)
        return paginator.get_paginated_response(self.get_serializer(queryset, many=True).data)

    @action(methods=["GET"], detail=True, url_path="task", url_name="task")
    def task(self, request, pk):
        """Video darsga task"""
        try:
            return Response(self.get_serializer(self.get_object()).data)
        except TutorialModel.DoesNotExist:
            raise NotFound(_("Tutorial not found"))

    @action(methods=["POST"], detail=True, url_path="task-answer", url_name="task-answer")
    def task_answer(self, request, pk):
        """Task javobini tekshirish"""
        try:
            tutorial = TutorialModel.objects.get(pk=pk)
        except TutorialModel.DoesNotExist:
            raise NotFound("Tutorial not found")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if tutorial.task.is_file_answer and "file" not in data:
            raise ValidationError({"file": ["Fayil yuborish majburiy"]})

        task = self.get_queryset()
        task_result, __ = TaskResultModel.objects.update_or_create(
            user=request.user,
            task=task,
            tutorial_id=pk,
            defaults={"answer": data.get("answer", None)},
        )
        if "file" in data:
            task_result.file.save(data["file"].name, data["file"])

        return Response({"detail": _("Task javobi qabul qilindi.")})

    @action(methods=["GET"], detail=False, url_name="is-full-completed", url_path="is-full-completed")
    def is_full_completed(self, request):
        completed = TutorialModel.objects.filter(users__in=[request.user]).count()
        total = TutorialModel.objects.count()
        return Response({"detail": total == completed})
