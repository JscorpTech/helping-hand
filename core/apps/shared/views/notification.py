from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated  # noqa
from core.apps.accounts.permissions import AdminPermission  # noqa
from rest_framework.viewsets import ModelViewSet
from ..models import NotificationModel, UserNotificationModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from ..serializers import (
    CreateNotificationSerializer,
    # ListNotificationSerializer,  # noqa
    RetrieveNotificationSerializer,
    UserNotificationSerializer,
)


@extend_schema(tags=["notification"])
class NotificationView(BaseViewSetMixin, ModelViewSet):
    queryset = NotificationModel.objects.all()
    filter_backends = [SearchFilter]
    search_fields = [
        "title_uz",
        "title_kaa",
        "title_kril",
        "body_uz",
        "body_kaa",
        "body_kril",
    ]

    def get_serializer_class(self) -> Any:
        match self.action:
            case "create":
                return CreateNotificationSerializer
            case "list":
                return UserNotificationSerializer
            case "retrieve":
                return RetrieveNotificationSerializer
            case _:
                return UserNotificationSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case "list":
                perms.extend([IsAuthenticated])
            case _:
                perms.extend([IsAuthenticated, AdminPermission])
        self.permission_classes = perms
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        user_notifications = UserNotificationModel.objects.filter(user=self.request.user)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(user_notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
