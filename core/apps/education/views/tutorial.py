from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from ..models import TutorialModel
from rest_framework.response import Response
from ..serializers.tutorial import CreateTutorialSerializer, ListTutorialSerializer, RetrieveTutorialSerializer
from ..serializers.test import RetrieveTestSerializer


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
                return TutorialModel.objects.all()

    @action(methods=["GET"], detail=True, url_path="test", url_name="test")
    def test(self, request, pk=None):
        return Response(self.get_serializer(self.get_queryset()).data)

    def get_serializer_class(self) -> Any:
        match self.action:
            case "list":
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
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()
