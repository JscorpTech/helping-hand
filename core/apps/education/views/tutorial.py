from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.apps.accounts.permissions import IsModeratorPermission


from ..models import TutorialModel, AnswerModel
from ..serializers.test import RetrieveTestSerializer
from django_core.paginations import CustomPagination
from ..serializers.tutorial import CreateTutorialSerializer, ListTutorialSerializer, RetrieveTutorialSerializer
from rest_framework.filters import SearchFilter
from ..serializers.test import AnswerSerializer
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _


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

    @extend_schema(request=AnswerSerializer)
    @action(methods=["POST"], detail=True, url_path="test-answer", url_name="test-answer")
    def test_answer(self, request, pk=None):
        """Test javoblarini tekshirish"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        test = self.get_queryset()
        questions = test.questions.all()
        success = 0

        if len(data) != len(questions):
            raise ValidationError({"detail": _("test javoblar soni noto'g'ri")})

        for i in data:
            question = i["question"]
            variants = i["variant"]
            if not question.is_many and len(variants) > 1:
                raise ValidationError({"detail": _("variantlar soni 1 ta bo'lishi kerak")})
            answer, __ = AnswerModel.objects.get_or_create(user=request.user, question=question, tutorial_id=pk)
            for j in variants:
                answer.variant.add(j)
                if j.is_true:
                    success += 1
        TutorialModel.objects.get(pk=pk).users.add(request.user)
        return Response(
            {"detail": _("Test javoblari qabul qildi"), "success": success, "total": len(questions)},
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
