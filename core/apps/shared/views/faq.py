from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.apps.accounts.permissions import AdminPermission
from rest_framework.viewsets import ModelViewSet

from ..models import FaqModel, FaqCategoryModel
from ..serializers import (
    CreateFaqSerializer,
    ListFaqSerializer,
    RetreiveFaqSerializer,
    CreateFaqCategorySerializer,
    ListFaqCategorySerializer,
    RetreiveFaqCategorySerializer,
    FaqsSerializer,
)

from rest_framework.filters import SearchFilter


@extend_schema(tags=["faq-category"])
class FaqCategoryView(BaseViewSetMixin, ModelViewSet):
    queryset = FaqCategoryModel.objects.all()
    filter_backends = [SearchFilter]
    search_fields = [
        "name_uz",
        "name_kaa",
        "name_kril",
    ]

    def get_serializer_class(self) -> Any:
        match self.action:
            case "create":
                return CreateFaqCategorySerializer
            case "list":
                return FaqsSerializer
            case "retreive":
                return RetreiveFaqCategorySerializer
            case _:
                return ListFaqCategorySerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case "create" | "update" | "partial_update" | "destroy":
                perms.extend([IsAuthenticated, AdminPermission])
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        self.permission_classes = [AllowAny]
        return super().get_permissions()


@extend_schema(tags=["faq"])
class FaqView(BaseViewSetMixin, ModelViewSet):
    queryset = FaqModel.objects.all()
    filter_backends = [SearchFilter]
    search_fields = [
        "question_uz",
        "question_kaa",
        "question_kril",
        "answer_uz",
        "answer_kaa",
        "answer_kril",
    ]

    def get_serializer_class(self) -> Any:
        match self.action:
            case "create":
                return CreateFaqSerializer
            case "list":
                return ListFaqSerializer
            case "retreive":
                return RetreiveFaqSerializer
            case _:
                return ListFaqSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case "create" | "update" | "partial_update" | "destroy":
                perms.extend([IsAuthenticated, AdminPermission])
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        self.permission_classes = [AllowAny]
        return super().get_permissions()
