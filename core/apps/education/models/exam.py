from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from rest_framework.exceptions import NotFound

from ..choices import SertificateChoices
from ..models.test import TestModel
from ..choices import TutorialTypeChoice


class ExamModel(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255)
    is_active = models.BooleanField(_("is active"), default=False, unique=True)
    tutorial_type = models.CharField(verbose_name=_("tutorial type"), choices=TutorialTypeChoice.choices, default=TutorialTypeChoice.LAWYER.value)
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
    user = models.ForeignKey(
        to=get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE, related_name="sertificates"
    )
    tutorial_type = models.CharField(verbose_name=_("tutorial type"), choices=TutorialTypeChoice.choices, default=TutorialTypeChoice.LAWYER.value)
    status = models.CharField(
        _("status"), max_length=255, choices=SertificateChoices.choices, default=SertificateChoices.DRAFT.value
    )
    file = models.FileField(_("file"), upload_to="sertificates/", null=True, blank=True)

    def __str__(self):
        return self.user.full_name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            user=get_user_model()._create_fake(),
            file="file.pdf",
        )

    class Meta:
        db_table = "sertificate"
        verbose_name = _("SertificateModel")
        verbose_name_plural = _("SertificateModels")


class ExamResultModel(AbstractBaseModel):
    user = models.ForeignKey(to=get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    tutorial_type = models.CharField(verbose_name=_("tutorial type"), choices=TutorialTypeChoice.choices, default=TutorialTypeChoice.LAWYER.value)
    bal = models.IntegerField(default=0)

    def __str__(self):
        return self.user.full_name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            user=get_user_model()._create_fake(),
            score=10,
            total=10,
            bal=10,
        )

    class Meta:
        db_table = "examresult"
        verbose_name = _("ExamresultModel")
        verbose_name_plural = _("ExamresultModels")
