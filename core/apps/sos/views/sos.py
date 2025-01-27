from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import models

from ..models import UserRequestModel
from ..serializers.sos import (
    CreateUserRequestSerializer,
    ListUserRequestSerializer,
    RetrieveUserRequestSerializer,
    TopRequestsSerializer,
)


@extend_schema(tags=["sos"])
class UserRequestView(BaseViewSetMixin, CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """Xafli hudud — unsafe
    Xafsiz hudud — safe"""

    queryset = UserRequestModel.objects.order_by("-created_at").all()

    @action(methods=["GET"], detail=False, url_name="top-users", url_path="top-users")
    def top_users(self, request):
        users = (
            get_user_model().objects.annotate(requests_count=models.Count("sos_requests")).order_by("-requests_count")
        )
        data = []
        for user in users:
            data.append(
                {
                    "count": user.requests_count,
                    "user": user,
                }
            )
        return Response(self.get_serializer(data, many=True).data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self) -> Any:
        match self.action:
            case "list":
                return ListUserRequestSerializer
            case "retrieve":
                return RetrieveUserRequestSerializer
            case "create":
                return CreateUserRequestSerializer
            case "top_users":
                return TopRequestsSerializer
            case _:
                return ListUserRequestSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case _:
                perms.extend([IsAuthenticated])
        self.permission_classes = perms
        return super().get_permissions()
