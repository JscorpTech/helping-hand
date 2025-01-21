from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.apps.accounts.permissions import AdminPermission
from rest_framework.viewsets import ModelViewSet

from ..models import FaqModel
from ..serializers.faq import CreateFaqSerializer, ListFaqSerializer, RetreiveFaqSerializer


@extend_schema(tags=["faq"])
class FaqView(BaseViewSetMixin, ModelViewSet):
    queryset = FaqModel.objects.all()

    def get_serializer_class(self):
        match self.action:
            case "create":
                return CreateFaqSerializer
            case "list":
                return ListFaqSerializer
            case "retreive":
                return RetreiveFaqSerializer
            case _:
                ListFaqSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case "create" | "update" | "partial_update" | "destroy":
                perms.extend([IsAuthenticated, AdminPermission])
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()