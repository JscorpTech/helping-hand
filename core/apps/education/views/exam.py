from typing import Any

from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from ..models import ExamModel, SertificateModel, ExamResultModel
from ..serializers.exam import (
    CreateSertificateSerializer,
    ListExamSerializer,
    ListSertificateSerializer,
    RetrieveSertificateSerializer,
    RetrieveExamSerializer,
)
from ..services import TestService
from ..serializers.test import AnswerSerializer


@extend_schema(tags=["exam"], summary="Imtixon")
class ExamView(BaseViewSetMixin, GenericViewSet):
    queryset = ExamModel.objects.all()

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
class SertificateView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = SertificateModel.objects.all()

    def get_serializer_class(self) -> Any:
        match self.action:
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
            case _:
                perms.extend([AllowAny])
        self.permission_classes = perms
        return super().get_permissions()
