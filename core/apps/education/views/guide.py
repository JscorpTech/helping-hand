from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..models import GuideModel
from ..serializers.guide import CreateGuideSerializer, ListGuideSerializer, RetrieveGuideSerializer


@extend_schema(tags=["guide"])
class GuideView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = GuideModel.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["guide_type"]
    search_fields = ["name", "desc"]

    def get_serializer_class(self) -> Any:
        match self.action:
            case "list":
                return ListGuideSerializer
            case "retrieve":
                return RetrieveGuideSerializer
            case "create":
                return CreateGuideSerializer
            case _:
                return ListGuideSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()
