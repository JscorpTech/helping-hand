from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from core.apps.accounts.permissions import IsModeratorPermission

from ..models import PostModel
from ..serializers.post import CreatePostSerializer, ListPostSerializer, RetrievePostSerializer


@extend_schema(tags=["post"])
class PostView(BaseViewSetMixin, ModelViewSet):

    def get_queryset(self):
        return PostModel.objects.order_by("-created_at")

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
