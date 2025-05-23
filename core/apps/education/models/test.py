from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel

from .tutorial import TutorialModel
from ..choices import TutorialTypeChoice


class TestModel(AbstractBaseModel):
    topic = models.CharField(_("topic"), max_length=255)
    desc = models.TextField(_("description"), blank=True, null=True)
    time = models.PositiveIntegerField(_("time"), default=0)
    tutorial_type = models.CharField(
        verbose_name=_("tutorial type"), choices=TutorialTypeChoice.choices, default=TutorialTypeChoice.LAWYER.value
    )

    def __str__(self):
        return self.topic

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            topic="Test",
            desc="Test",
            time=0,
        )

    class Meta:
        db_table = "test"
        verbose_name = _("TestModel")
        verbose_name_plural = _("TestModels")


class QuestionModel(AbstractBaseModel):
    test = models.ForeignKey("TestModel", verbose_name=_("test"), on_delete=models.CASCADE, related_name="questions")
    question = models.TextField(_("question"))
    is_any = models.BooleanField(_("is any"), default=False)
    is_many = models.BooleanField(_("is many"), default=False)

    def __str__(self):
        return self.question[:100]

    class Meta:
        db_table = "question"
        verbose_name = _("QuestionModel")
        verbose_name_plural = _("QuestionModels")


class VariantModel(AbstractBaseModel):
    question = models.ForeignKey(
        "QuestionModel", verbose_name=_("question"), on_delete=models.CASCADE, related_name="variants"
    )
    variant = models.CharField(_("variant"), max_length=1000)
    bal = models.IntegerField()
    is_true = models.BooleanField(_("is true"), default=False)

    def __str__(self):
        return "%s..." % self.variant[:100]

    class Meta:
        db_table = "variant"
        verbose_name = _("VariantModel")
        verbose_name_plural = _("VariantModels")


class ResultModel(AbstractBaseModel):
    user = models.ForeignKey(get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE, related_name="results")
    tutorial = models.ForeignKey(
        "TutorialModel", verbose_name=_("tutorial"), on_delete=models.CASCADE, related_name="results"
    )
    score = models.PositiveIntegerField(_("score"), default=0)
    total = models.PositiveIntegerField(_("total"), default=0)
    bal = models.IntegerField(default=0)

    def __str__(self):
        return self.user.full_name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            user=get_user_model()._create_fake(),
            tutorial=TutorialModel._create_fake(),
            score=10,
        )

    class Meta:
        db_table = "result"
        verbose_name = _("ResultModel")
        verbose_name_plural = _("ResultModels")
        unique_together = (
            "user",
            "tutorial",
        )
