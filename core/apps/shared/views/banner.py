from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import BannerModel
from ..serializers.banner import CreateBannerSerializer, ListBannerSerializer, RetrieveBannerSerializer


@extend_schema(tags=["banner"])
class BannerView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = BannerModel.objects.all()

    def get_serializer_class(self) -> Any:
        match self.action:
            case "list":
                return ListBannerSerializer
            case "retrieve":
                return RetrieveBannerSerializer
            case "create":
                return CreateBannerSerializer
            case _:
                return ListBannerSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()
