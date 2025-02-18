from typing import Any

from django.shortcuts import get_object_or_404
from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..models import QuestionModel
from ..serializers.test import (
    CreateQuestionBulkSerializer,
    CreateQuestionSerializer,
    ListQuestionSerializer,
    RetrieveQuestionSerializer,
)


@extend_schema(tags=["question"])
class QuestionView(
    BaseViewSetMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet
):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["test", "is_any", "is_many"]
    search_fields = [
        "question_uz",
        "question_kaa",
        "question_kril",
    ]

    def get_queryset(self):
        query = QuestionModel.objects.all()
        match self.action:
            case _:
                return query

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get("pk"))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"detail": "Question created"}, status=201)

    def get_serializer_class(self) -> Any:
        match self.action:
            case "create":
                return CreateQuestionBulkSerializer
            case "update" | "partial_update":
                return CreateQuestionSerializer
            case "retrieve":
                return RetrieveQuestionSerializer
            case _:
                return ListQuestionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["action"] = self.action
        return context

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()
