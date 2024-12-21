from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from ..choices import TutorialTypeChoice


class TutorialModel(AbstractBaseModel):
    type = models.CharField(
        _("type"), max_length=255, choices=TutorialTypeChoice.choices, default=TutorialTypeChoice.MANUAL
    )
    name = models.CharField(_("name"), max_length=255)
    desc = models.TextField(_("description"), blank=True, null=True)
    image = models.ImageField(_("banner"), upload_to="tutorials/")
    file = models.FileField(_("file"), upload_to="tutorials/", blank=True, null=True)
    video = models.FileField(_("video"), upload_to="tutorials/", blank=True, null=True)
    test = models.ForeignKey(
        "TestModel", verbose_name=_("test"), on_delete=models.CASCADE, related_name="tutorials", blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tutorial"
        verbose_name = _("TutorialModel")
        verbose_name_plural = _("TutorialModels")
