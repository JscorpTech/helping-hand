from typing import Any

from django_core.mixins import BaseViewSetMixin
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from ..models import GuideModel
from ..serializers.guide import CreateGuideSerializer, ListGuideSerializer, RetrieveGuideSerializer


@extend_schema(tags=["guide"], summary="Qo'llanma")
class GuideView(BaseViewSetMixin, ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["guide_type"]
    search_fields = ["name", "desc"]

    def get_queryset(self):
        match self.action:
            case "videos":
                # Video qo'llanmalarini qaytaradi
                return GuideModel.objects.filter(video__isnull=False).exclude(video="")
            case "files":
                # Foydalanuvchi qo'llanmalarini qaytaradi
                return GuideModel.objects.filter(file__isnull=False).exclude(file="")
            case _:
                return GuideModel.objects.all()

    @extend_schema(
        summary="Video qo'llanmalar ro'yxatini qaytaradi",
        responses={200: ListGuideSerializer(many=True)},
    )
    @action(methods=["GET"], detail=False, url_path="videos", url_name="videos")
    def videos(self, request, *args, **kwargs):
        """Video qo'llanmalar ro'yxatini qaytaradi"""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Foydalanuvchi qo'llanmalar ro'yxatini qaytaradi",
        responses={200: ListGuideSerializer(many=True)},
    )
    @action(methods=["GET"], detail=False, url_path="files", url_name="files")
    def files(self, request, *args, **kwargs):
        """Foydalanuvchi qo'llanmalar ro'yxatini qaytaradi"""
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Qo'llanma detail", responses={200: RetrieveGuideSerializer})
    def retrieve(self, request, *args, **kwargs):
        """Qo'llanma detail"""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="Qo'llanma list", responses={200: ListGuideSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        """Qo'llanma list"""
        return super().list(request, *args, **kwargs)

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

