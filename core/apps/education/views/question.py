from typing import Any

from django.utils.translation import gettext as _
from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from ..models import QuestionModel
from django.shortcuts import get_object_or_404


from ..serializers.test import CreateQuestionSerializer, RetrieveQuestionSerializer, ListQuestionSerializer


@extend_schema(tags=["question"])
class QuestionView(
    BaseViewSetMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet
):

    def get_queryset(self):
        query = QuestionModel.objects.all()
        match self.action:
            case _:
                return query

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get("pk"))

    def get_serializer_class(self) -> Any:
        match self.action:
            case "create" | "update" | "partial_update":
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
