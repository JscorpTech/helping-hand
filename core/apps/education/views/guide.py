from typing import Any

from django_core.mixins import BaseViewSetMixin
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from ..models import GuideModel, TutorialTypeChoice
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
                queryset = GuideModel.objects.filter(video__isnull=False).exclude(video="")
            case "files":
                # Foydalanuvchi qo'llanmalarini qaytaradi
                queryset = GuideModel.objects.filter(file__isnull=False).exclude(file="")
            case _:
                queryset = GuideModel.objects.all()
        guide_type = self.request.query_params.get("guide_type", None)
        if not guide_type == TutorialTypeChoice.DOCUMENT:
            queryset = queryset.exclude(guide_type=TutorialTypeChoice.DOCUMENT)
        print(queryset)
        return queryset

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

    @extend_schema(
        summary="Dokument",
        responses={200: ListGuideSerializer(many=True)},
    )
    @action(methods=["GET"], detail=False, url_path="document", url_name="document")
    def document(self, request, *args, **kwargs):
        wanted = request.query_params.get("guide_type")
        if wanted:
            qs = GuideModel.objects.filter(Q(guide_type=wanted) | Q(guide_type=TutorialTypeChoice.DOCUMENT))
        else:
            qs = GuideModel.objects.all()

        search = request.query_params.get("search")
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(desc__icontains=search))

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = ListGuideSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = ListGuideSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)

    def get_serializer_class(self) -> Any:
        match self.action:
            case "list":
                return ListGuideSerializer
            case "retrieve":
                return RetrieveGuideSerializer
            case "create" | "update" | "partial_update":
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
