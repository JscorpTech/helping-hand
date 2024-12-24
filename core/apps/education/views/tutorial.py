from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import TutorialModel
from ..serializers.test import RetrieveTestSerializer
from django_core.paginations import CustomPagination
from ..serializers.tutorial import CreateTutorialSerializer, ListTutorialSerializer, RetrieveTutorialSerializer


@extend_schema(tags=["tutorial"])
class TutorialView(BaseViewSetMixin, ReadOnlyModelViewSet):

    def get_queryset(self):
        match self.action:
            case "test":
                return (
                    TutorialModel.objects.select_related("test")
                    .prefetch_related("test__questions", "test__questions__variants")
                    .get(pk=self.kwargs.get("pk"))
                    .test
                )
            case _:
                return TutorialModel.objects.prefetch_related("users").order_by("position").all()

    @action(methods=["GET"], detail=True, url_path="test", url_name="test")
    def test(self, request, pk=None):
        """Video darsga test"""
        return Response(self.get_serializer(self.get_queryset()).data)

    @extend_schema(
        responses={200: ListTutorialSerializer(many=True)},
    )
    @action(methods=["GET"], detail=False, url_path="completed", url_name="completed")
    def completed(self, request):
        """Yakunlangan video darslar"""
        queryset = self.get_queryset().filter(users__in=[request.user])
        paginator = CustomPagination()
        queryset = paginator.paginate_queryset(queryset, request)
        return paginator.get_paginated_response(self.get_serializer(queryset, many=True).data)

    def paginate_queryset(self, queryset):
        return super().paginate_queryset(queryset)

    def get_serializer_class(self) -> Any:
        match self.action:
            case "list" | "completed":
                return ListTutorialSerializer
            case "retrieve":
                return RetrieveTutorialSerializer
            case "create":
                return CreateTutorialSerializer
            case "test":
                return RetrieveTestSerializer
            case _:
                return ListTutorialSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case "completed":
                perms.extend([IsAuthenticated])
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()
