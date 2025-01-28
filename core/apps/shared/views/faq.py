from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import FaqCategoryModel, FaqModel
from ..serializers import (
    CreateFaqCategorySerializer,
    CreateFaqSerializer,
    CsListFaqCategorySerializer,
    FaqsSerializer,
    ListFaqCategorySerializer,
    ListFaqSerializer,
    RetreiveFaqCategorySerializer,
)


@extend_schema(tags=["faq-category"])
class FaqCategoryView(BaseViewSetMixin, ModelViewSet):
    queryset = FaqCategoryModel.objects.all()

    def get_serializer_class(self) -> Any:
        match self.action:
            case "create":
                return CreateFaqCategorySerializer
            case "list":
                return FaqsSerializer
            case "retrieve":
                return RetreiveFaqCategorySerializer
            case "faq_categories":
                return CsListFaqCategorySerializer
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

    @extend_schema(summary="FAQ categories", description="FAQ categories list")
    @action(detail=False, methods=["GET"], url_path="faq-categories")
    def faq_categories(self, request) -> Any:
        print(request.headers)
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=["faq"])
class FaqView(BaseViewSetMixin, ModelViewSet):
    queryset = FaqModel.objects.all()

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
