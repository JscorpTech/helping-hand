from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated  # noqa
from core.apps.accounts.permissions import AdminPermission
from rest_framework.viewsets import ModelViewSet
from typing import Any

from ..models import NotificationModel, UserNotificationModel

# from rest_framework.response import Response
# from rest_framework import status
from ..serializers import (  # ListNotificationSerializer,  # noqa
    CreateNotificationSerializer,
    NotificationSerializer,
    RetrieveNotificationSerializer,
    UserNotificationSerializer,
)


@extend_schema(tags=["notification"])
class NotificationView(BaseViewSetMixin, ModelViewSet):
    queryset = NotificationModel.objects.all()

    def get_serializer_class(self) -> Any:
        match self.action:
            case "create":
                return CreateNotificationSerializer
            case "list":
                return UserNotificationSerializer
            case "retrieve":
                return RetrieveNotificationSerializer
            case "notifications":
                return NotificationSerializer
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
        paginator = self.paginator
        serializer_class = self.get_serializer_class()
        paginated_queryset = paginator.paginate_queryset(user_notifications, request, view=self)
        serializer = serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(summary="All notifications", description="All notifications")
    @action(detail=False, methods=["GET"], url_path="notifications")
    def notifications(self, request, *args, **kwargs):
        notifications = NotificationModel.objects.all()
        paginator = self.paginator
        serializer_class = self.get_serializer_class()
        paginated_queryset = paginator.paginate_queryset(notifications, request, view=self)
        serializer = serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
