from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class GuideModel(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def _create_face(self):
        return self.objects.create(
            name="Test",
        )

    class Meta:
        db_table = "guide"
        verbose_name = _("GuideModel")
        verbose_name_plural = _("GuideModels")
