from typing import Any

from django.db import transaction
from django.utils.translation import gettext as _
from django_core.mixins import BaseViewSetMixin
from django_core.paginations import CustomPagination
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from core.apps.accounts.permissions import AdminPermission

from ..choices import ProgressChoices
from ..models import ResultModel, TaskResultModel, TutorialModel, TestModel
from ..serializers.task import RetrieveTaskSerializer, TaskAnswerSerializer
from ..serializers.test import (
    CreateQuestionSerializer,
    CreateTestSerializer,
    RetrieveTestSerializer,
    UpdateTestSerializer,
)
from ..serializers.test.answer import AnswerSerializer
from ..serializers.tutorial import (
    CreateTutorialSerializer,
    ListProgressSerializer,
    ListTutorialSerializer,
    RetrieveTutorialSerializer,
)
from ..services import TestService


@extend_schema(
    tags=["tutorial"],
    parameters=[
        OpenApiParameter(name="search", type=str, description="Search by name, desc, tags"),
    ],
)
class TutorialView(BaseViewSetMixin, ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = [
        "test",
    ]
    search_fields = ["name_uz", "name_kaa", "name_kril", "desc_uz", "desc_kaa", "desc_kril", "tags"]

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
            case "test_update":
                return UpdateTestSerializer
            case "task":
                return RetrieveTaskSerializer
            case "task_answer":
                return TaskAnswerSerializer
            case "progress":
                return ListProgressSerializer
            case "create_test":
                return CreateTestSerializer
            case "test_answer":
                return AnswerSerializer
            case "update_question":
                return CreateQuestionSerializer
            case _:
                return ListTutorialSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case "create" | "update" | "partial_update" | "destroy" "create_test":
                perms.extend([IsAuthenticated, AdminPermission])
            case "test_answer" | "task_answer" | "is_full_completed" | "completed":
                perms.extend([IsAuthenticated])
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()

    @extend_schema(
        summary="Test yaratish",
        request=CreateTestSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string"},
                        "test": {"type": "integer"},
                    },
                }
            )
        },
    )
    @action(methods=["POST"], detail=True, url_path="create-test", url_name="create-test")
    def create_test(self, request, pk=None):
        """Test yaratish uchun"""
        tutorial = self.get_object()
        serializer = self.get_serializer(data=request.data, context={"tutorial": tutorial})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response({"detail": _("Test yaratildi."), "test": data.id}, status=201)

    @extend_schema(
        summary="Test javoblarini tekshirish",
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
        """Test javoblarini tekshirish uchun"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        test = get_object_or_404(TestModel, pk=pk)
        questions = test.questions.all()

        if len(data) != len(questions):
            raise ValidationError({"question": [_("Test javoblar soni noto'g'ri.")]})

        success = 0
        bal = 0

        with transaction.atomic():
            for item in data:
                question = item["question"]
                variants = item["variant"]
                TestService.check_answer_validity(question, variants)
                s, b = TestService().calculate_score_and_balance(question, variants)
                success += s
                bal += b

            TutorialModel.objects.get(pk=test.tutorials.first().id).users.add(request.user)
            ResultModel.objects.update_or_create(
                user=request.user,
                tutorial_id=pk,
                defaults={"score": success, "total": len(questions), "bal": bal},
            )

            return Response(
                {"detail": _("Test javoblari qabul qilindi."), "success": success, "total": len(questions), "bal": bal}
            )

    @extend_schema(
        summary="Darslik uchun testni olish",
        description="Darsga berilgan testni olish",
    )
    @action(methods=["GET"], detail=True, url_path="test", url_name="test")
    def test(self, request, pk=None):
        """Darslik uchun testni olish uchun"""
        try:
            return Response(self.get_serializer(self.get_queryset()).data)
        except TutorialModel.DoesNotExist:
            raise NotFound(_("Tutorial not found"))

    @extend_schema(
        summary="Testni update qilish (PATCH)",
        description="Testni update qilish (PATCH)",
    )
    @action(methods=["PATCH"], detail=True, url_path="test-update", url_name="test-update")
    def test_update(self, request, pk=None):
        """Testni update qilish (PATCH)"""
        try:
            test = self.get_queryset().get(pk=pk).test
            serializer = self.get_serializer(test, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=400)
        except TutorialModel.DoesNotExist:
            raise NotFound(_("Tutorial not found"))

    @extend_schema(
        summary="Yakunganlan video darslarni ro'yhatini olish",
        responses={200: ListTutorialSerializer(many=True)},
    )
    @action(methods=["GET"], detail=False, url_path="completed", url_name="completed")
    def completed(self, request):
        """Yakunlangan video darslar ro'yhatini olish uchun"""
        queryset = self.get_queryset().filter(users__in=[request.user])
        paginator = CustomPagination()
        queryset = paginator.paginate_queryset(queryset, request)
        return paginator.get_paginated_response(self.get_serializer(queryset, many=True).data)

    @action(methods=["GET"], detail=True, url_path="task", url_name="task")
    def task(self, request, pk):
        """Darslik uchun topshiriqni olish uchun"""
        try:
            return Response(self.get_serializer(self.get_object()).data)
        except TutorialModel.DoesNotExist:
            raise NotFound(_("Tutorial not found"))

    @action(methods=["POST"], detail=True, url_path="task-answer", url_name="task-answer")
    def task_answer(self, request, pk):
        """Topshiriq javoblarini tekshirish uchun"""
        try:
            tutorial = TutorialModel.objects.get(pk=pk)
        except TutorialModel.DoesNotExist:
            raise NotFound("Tutorial not found")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if tutorial.task.is_file_answer and "file" not in data:
            raise ValidationError({"file": ["Fayil yuborish majburiy"]})
        task = self.get_object()
        task_result, __ = TaskResultModel.objects.update_or_create(
            user=request.user,
            task=task,
            tutorial_id=pk,
            defaults={"answer": data.get("answer", None)},
        )
        if "file" in data:
            task_result.file.save(data["file"].name, data["file"])

        return Response({"detail": _("Task javobi qabul qilindi.")})

    @extend_schema(
        responses=OpenApiResponse(
            response={"type": "object", "properties": {"detail": {"type": "boolean", "example": False}}}
        )
    )
    @action(methods=["GET"], detail=False, url_name="is-full-completed", url_path="is-full-completed")
    def is_full_completed(self, request):
        """Barcha kurslarni yakunlaganini tekshirish uchun"""
        completed = TutorialModel.objects.filter(users__in=[request.user]).count()
        total = TutorialModel.objects.count()
        return Response({"detail": total == completed})

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "example": 1},
                            "status": {
                                "type": "string",
                                "example": "NOT_STARTED",
                                "enum": ["NOT_STARTED", "IN_PROGRESS", "COMPLETED"],
                            },
                        },
                    },
                }
            )
        }
    )
    @action(methods=["GET"], detail=False, url_name="progress", url_path="progress")
    def progress(self, request):
        """Darsliklar progressini ko'rish uchun"""
        query = self.get_queryset()
        data = []
        previous_passed = True
        for item in query.all():
            is_passed = item.users.filter(id=request.user.id).exists()
            if is_passed:
                status = ProgressChoices.COMPLETED
            elif previous_passed:
                status = ProgressChoices.IN_PROGRESS
            else:
                status = ProgressChoices.NOT_STARTED
            data.append({"id": item.id, "name": _("%s-dars") % item.position, "status": status})
            previous_passed = is_passed
        return Response(self.get_serializer(data, many=True).data)
