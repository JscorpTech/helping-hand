from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.apps.accounts.permissions import AdminPermission

from ..models import BannerModel
from ..serializers.banner import CreateBannerSerializer, ListBannerSerializer, RetrieveBannerSerializer
from rest_framework.filters import SearchFilter


@extend_schema(tags=["banner"])
class BannerView(BaseViewSetMixin, ModelViewSet):
    queryset = BannerModel.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["title_uz", "title_kaa", "title_kril", "subtitle_uz", "subtitle_kaa", "subtitle_kril"]

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
            case "create" | "update" | "partial_update" | "destroy":
                perms.extend([IsAuthenticated, AdminPermission])
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()
