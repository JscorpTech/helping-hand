from typing import Any

from django.utils.translation import gettext_lazy as _
from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from core.apps.accounts.permissions import AdminPermission

from ..models import ExamModel, ExamResultModel, SertificateModel
from ..serializers.exam import (
    CreateSertificateSerializer,
    ListExamSerializer,
    ListMeSertificateSerializer,
    ListSertificateSerializer,
    RetrieveExamSerializer,
    RetrieveSertificateSerializer,
)
from ..serializers.test import AnswerSerializer
from ..services import TestService


@extend_schema(tags=["exam"], summary="Imtixon")
class ExamView(BaseViewSetMixin, GenericViewSet):
    queryset = ExamModel.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["test", "is_active"]
    search_fields = ["name"]

    @action(methods=["GET"], detail=False, url_name="exam", url_path="exam")
    def exam(self, request):
        """Imtixon uchun testlarni olish"""
        return Response(self.get_serializer(ExamModel.get_exam()).data)

    @extend_schema(request=AnswerSerializer)
    @action(methods=["POST"], detail=False, url_name="exam-answer", url_path="exam-answer")
    def exam_answer(self, request):
        """Imtixon javoblarini yuborish"""
        exam = ExamModel.get_exam()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        test = exam.test
        questions = test.questions.all()

        if len(data) != len(questions):
            raise ValidationError({"question": [_("Test javoblar soni noto'g'ri.")]})

        success, bal = TestService().proccess_answers(data)

        ExamResultModel.objects.update_or_create(
            user=request.user,
            exam=exam,
            defaults={"score": success, "total": len(questions), "bal": bal},
        )
        SertificateModel.objects.get_or_create(user=request.user, exam=exam)

        return Response(
            {"detail": _("Test javoblari qabul qilindi."), "success": success, "total": len(questions), "bal": bal}
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

    @action(methods=["GET"], detail=False, url_name="me", url_path="me")
    def me(self, request):
        return Response(self.get_serializer(SertificateModel.objects.filter(user=request.user).first()).data)

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
