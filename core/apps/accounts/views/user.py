from django.utils.translation import gettext_lazy as _  # noqa
from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from ..permissions import AdminPermission

from ..serializers import (
    UserCreateSerializer,
    UserListSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer,
)



@extend_schema(tags=["user"])
class UserView(BaseViewSetMixin, ModelViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, AdminPermission]

    def get_serializer_class(self):
        match self.action:
            case "create":
                return UserCreateSerializer
            case "update":
                return UserUpdateSerializer
            case "list":
                return UserListSerializer
            case "retreive":
                return UserRetrieveSerializer
            case _:
                return UserListSerializer
        return super().get_serializer_class()
