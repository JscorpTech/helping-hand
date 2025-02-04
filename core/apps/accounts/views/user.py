from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _  # noqa
from django_core.mixins import BaseViewSetMixin  # noqa
from drf_spectacular.utils import extend_schema  # noqa
from rest_framework.permissions import AllowAny, IsAuthenticated  # noqa
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from ..permissions import AdminPermission
from ..serializers import UserCreateSerializer, UserListSerializer, UserRetrieveSerializer, UserUpdateSerializer


@extend_schema(tags=["user"])
class UserView(BaseViewSetMixin, ModelViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, AdminPermission]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["role", "created_at", "validated_at"]
    search_fields = ["phone", "first_name", "last_name", "username"]

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
