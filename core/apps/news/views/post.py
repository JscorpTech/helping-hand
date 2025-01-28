from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_core.paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from core.apps.accounts.choices import RoleChoice
from rest_framework.filters import SearchFilter

from core.apps.accounts.permissions import AdminPermission

from ..models import PostModel
from ..serializers.post import CreatePostSerializer, ListPostSerializer, RetrievePostSerializer


@extend_schema(tags=["post"])
class PostView(BaseViewSetMixin, ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["news_type", "is_top"]
    search_fields = [
        "title_uz",
        "title_kaa",
        "title_kril",
        "content_uz",
        "content_kaa",
        "content_kril",
    ]

    def get_queryset(self):
        query = PostModel.objects.order_by("-created_at")
        if self.action in ["top_list"]:
            return query.filter(is_top=True)
        if self.action in ["list"]:
            if self.request.user.is_authenticated and self.request.user.role in RoleChoice.admin_roles():
                return query
            return query.filter(is_top=False)
        return query

    def get_serializer_class(self) -> Any:
        match self.action:
            case "list":
                return ListPostSerializer
            case "retrieve":
                return RetrievePostSerializer
            case "create":
                return CreatePostSerializer
            case _:
                return ListPostSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case "create" | "update" | "partial_update" | "destroy":
                perms.extend([IsAuthenticated, AdminPermission])
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()

    @extend_schema(responses={200: OpenApiResponse(response=CreatePostSerializer)})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.views += 1
        instance.save()
        return Response(serializer.data)

    @extend_schema(responses={200: OpenApiResponse(response=ListPostSerializer(many=True))})
    @action(methods=["GET"], detail=False, url_name="top-list", url_path="top-list")
    def top_list(self, request):
        pagination = CustomPagination()
        return pagination.get_paginated_response(
            self.get_serializer(
                pagination.paginate_queryset(self.filter_queryset(self.get_queryset()), request), many=True
            ).data
        )
