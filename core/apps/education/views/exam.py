from typing import Any

from django.utils.translation import gettext_lazy as _
from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError, NotFound

from core.apps.accounts.permissions import AdminPermission

from ..models import ExamModel, ExamResultModel, SertificateModel, TestModel
from ..serializers.exam import (
    CreateSertificateSerializer,
    ListExamSerializer,
    ListMeSertificateSerializer,
    ListSertificateSerializer,
    RetrieveExamSerializer,
    RetrieveSertificateSerializer,
)
from ..serializers.test import AnswerSerializer, RetrieveTestSerializer
from ..services import TestService
from ..choices import TutorialTypeChoice


@extend_schema(tags=["exam"], summary="Imtixon")
class ExamView(BaseViewSetMixin, GenericViewSet):
    queryset = ExamModel.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["test", "is_active"]
    search_fields = ["name"]

    @action(methods=["GET"], detail=False, url_name="exam", url_path="exam")
    def exam(self, request):
        """Imtixon uchun testlarni olish"""
        return Response({"id": 1, "test": RetrieveTestSerializer(TestModel.objects.order_by("?").first()).data})

    @extend_schema(request=AnswerSerializer)
    @action(methods=["POST"], detail=False, url_name="exam-answer", url_path="exam-answer")
    def exam_answer(self, request):
        """Imtixon javoblarini yuborish"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data_len = len(data)

        success, bal = TestService().proccess_answers(data)

        ExamResultModel.objects.update_or_create(
            user=request.user,
            defaults={"score": success, "total": data_len, "bal": bal},
        )
        SertificateModel.objects.get_or_create(user=request.user)

        return Response(
            {"detail": _("Test javoblari qabul qilindi."), "success": success, "total": data_len, "bal": bal}
        )

    def get_serializer_class(self) -> Any:
        match self.action:
            case "exam_answer":
                return AnswerSerializer
            case "exam":
                return RetrieveExamSerializer
            case _:
                return ListExamSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()


@extend_schema(tags=["sertificate"])
class SertificateView(BaseViewSetMixin, ModelViewSet):
    queryset = SertificateModel.objects.all()
    filter_backends = [SearchFilter]
    filterset_fields = ["user", "exam"]

    @action(methods=["GET"], detail=False, url_name="me", url_path="me/(?P<tutorial_type>[0-9a-zA-Z]+)")
    def me(self, request, tutorial_type):
        if tutorial_type not in TutorialTypeChoice.values:
            raise ValidationError({
                "tutorial_type": "tutorial type not allowed"
            })
        sertificate = SertificateModel.objects.filter(user=request.user, tutorial_type=tutorial_type).first()
        if sertificate is None:
            raise NotFound({"detail": _("Sertificate not found")})
        return Response(self.get_serializer().data)

    def get_serializer_class(self) -> Any:
        match self.action:
            case "me":
                return ListMeSertificateSerializer
            case "list":
                return ListSertificateSerializer
            case "retrieve":
                return RetrieveSertificateSerializer
            case "create":
                return CreateSertificateSerializer
            case _:
                return ListSertificateSerializer

    def get_permissions(self) -> Any:
        perms = []
        match self.action:
            case "create":
                perms.extend([IsAuthenticated, AdminPermission])
            case _:
                perms.extend([AllowAny, IsAuthenticated])
        self.permission_classes = perms
        return super().get_permissions()
