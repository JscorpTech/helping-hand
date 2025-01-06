from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_core.paginations import CustomPagination

from core.apps.accounts.permissions import IsModeratorPermission

from ..models import PostModel
from ..serializers.post import CreatePostSerializer, ListPostSerializer, RetrievePostSerializer


@extend_schema(tags=["post"])
class PostView(BaseViewSetMixin, ModelViewSet):

    def get_queryset(self):
        query = PostModel.objects.order_by("-created_at")
        match self.action:
            case "top_list":
                return query.filter(is_top=True)
            case "list":
                return query.filter(is_top=False)
            case _:
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
                perms.extend([IsModeratorPermission])
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.views += instance.views
        instance.save()
        return Response(serializer.data)

    @extend_schema(responses={200: OpenApiResponse(response=ListPostSerializer(many=True))})
    @action(methods=["GET"], detail=False, url_name="top-list", url_path="top-list")
    def top_list(self, request):
        pagination = CustomPagination()
        return pagination.get_paginated_response(
            self.get_serializer(pagination.paginate_queryset(self.get_queryset(), request), many=True).data
        )
