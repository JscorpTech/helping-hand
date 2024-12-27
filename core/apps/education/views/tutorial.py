from typing import Any

from django.utils.translation import gettext as _
from django_core.mixins import BaseViewSetMixin
from django_core.paginations import CustomPagination
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db import transaction

from core.apps.accounts.permissions import IsModeratorPermission

from ..models import AnswerModel, TutorialModel, ResultModel
from ..serializers.test import AnswerSerializer, RetrieveTestSerializer
from ..serializers.tutorial import CreateTutorialSerializer, ListTutorialSerializer, RetrieveTutorialSerializer


@extend_schema(
    tags=["tutorial"],
    parameters=[
        OpenApiParameter(name="search", type=str, description="Search by name, desc, tags"),
    ],
)
class TutorialView(BaseViewSetMixin, ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ["name", "desc", "tags"]

    def get_queryset(self):
        match self.action:
            case "test" | "test_answer":
                return (
                    TutorialModel.objects.select_related("test")
                    .prefetch_related("test__questions", "test__questions__variants")
                    .get(pk=self.kwargs.get("pk"))
                    .test
                )
            case _:
                return TutorialModel.objects.prefetch_related("users").order_by("position").all()

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
        answers = []

        with transaction.atomic():
            for item in data:
                question = item["question"]
                variants = item["variant"]

                # Tekshirish: Ko'p variantli savollar uchun cheklov
                if not question.is_many and len(variants) > 1:
                    raise ValidationError({"variant": [_("Variantlar soni 1 ta bo'lishi kerak.")]})

                # Tekshirish: Variantlarning to'g'riligi
                variant_ids = [variant.id for variant in variants]
                if question.variants.filter(id__in=variant_ids).count() != len(variants):
                    raise ValidationError({"variant": [_("Variantlar noto'g'ri tekshirilishi kerak.")]})

                # Javobni yaratish yoki yangilash
                answer, __ = AnswerModel.objects.get_or_create(user=request.user, question=question, tutorial_id=pk)
                answer.variant.set(variants)

                # To'g'ri javoblarni tekshirish
                correct_count = question.variants.filter(is_true=True).count()
                selected_correct = sum(1 for variant in variants if variant.is_true)

                if correct_count == selected_correct:
                    success += 1

                answers.append(answer)

            TutorialModel.objects.get(pk=pk).users.add(request.user)
            ResultModel.objects.update_or_create(
                user=request.user,
                tutorial_id=pk,
                defaults={"score": success, "total": len(questions)},
            )

            return Response(
                {
                    "detail": _("Test javoblari qabul qilindi."),
                    "success": success,
                    "total": len(questions),
                }
            )

    @action(methods=["GET"], detail=True, url_path="test", url_name="test")
    def test(self, request, pk=None):
        """Video darsga test"""
        return Response(self.get_serializer(self.get_queryset()).data)

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
            case _:
                return ListTutorialSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case "create" | "update" | "partial_update" | "destroy":
                perms.extend([IsAuthenticated, IsModeratorPermission])
            case "completed":
                perms.extend([IsAuthenticated])
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()
