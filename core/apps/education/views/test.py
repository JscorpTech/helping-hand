from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import AnswerModel
from ..serializers.test import CreateAnswerSerializer, ListAnswerSerializer, RetrieveAnswerSerializer


@extend_schema(tags=["answer"])
class AnswerView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = AnswerModel.objects.all()

    def get_serializer_class(self) -> Any:
        match self.action:
            case "list":
                return ListAnswerSerializer
            case "retrieve":
                return RetrieveAnswerSerializer
            case "create":
                return CreateAnswerSerializer
            case _:
                return ListAnswerSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()
