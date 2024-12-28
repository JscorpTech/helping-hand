from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from ..models.test import TestModel
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound


class ExamModel(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255)
    is_active = models.BooleanField(_("is active"), default=False, unique=True)
    test = models.ForeignKey(to="TestModel", verbose_name=_("test"), on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @classmethod
    def get_exam(self):
        exam = self.objects.filter(is_active=True)
        if not exam.exists():
            raise NotFound(_("Imtihon uchun savollar topilmadi iltimos admin bilan bog'laning"))
        return exam.first()

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="exam",
            is_active=True,
            test=TestModel._create_fake(),
        )

    class Meta:
        db_table = "exam"
        verbose_name = _("ExamModel")
        verbose_name_plural = _("ExamModels")


class SertificateModel(AbstractBaseModel):
    user = models.ForeignKey(to=get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE)
    file = models.FileField(_("file"), upload_to="sertificates/")
    exam = models.ForeignKey("ExamModel", verbose_name=_("exam"), on_delete=models.SET_NULL, null=True, blank=False)

    def __str__(self):
        return self.user.full_name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            user=get_user_model()._create_fake(),
            file="file.pdf",
            exam=ExamModel._create_fake(),
        )

    class Meta:
        db_table = "sertificate"
        verbose_name = _("SertificateModel")
        verbose_name_plural = _("SertificateModels")


class ExamResultModel(AbstractBaseModel):
    user = models.ForeignKey(to=get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE)
    exam = models.ForeignKey(to="ExamModel", verbose_name=_("exam"), on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    bal = models.IntegerField(default=0)

    def __str__(self):
        return self.user.full_name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            user=get_user_model()._create_fake(),
            exam=ExamModel._create_fake(),
            score=10,
            total=10,
            bal=10,
        )

    class Meta:
        db_table = "examresult"
        verbose_name = _("ExamresultModel")
        verbose_name_plural = _("ExamresultModels")
