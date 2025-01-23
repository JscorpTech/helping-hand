from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from ..models import UserRequestModel
from ..serializers.sos import CreateUserRequestSerializer, ListUserRequestSerializer, RetrieveUserRequestSerializer


@extend_schema(tags=["sos"])
class UserRequestView(BaseViewSetMixin, CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """Xafli hudud — dangerous
    Xafsiz hudud — unsafe"""

    queryset = UserRequestModel.objects.all()

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
            case _:
                return ListUserRequestSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case _:
                perms.extend([IsAuthenticated])
        self.permission_classes = perms
        return super().get_permissions()
