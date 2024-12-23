from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class PositionModel(AbstractBaseModel):
    location = models.PointField(_("location"), srid=4326)
    user = models.ForeignKey(verbose_name=_("user"), to=get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return "Object: %s" % self.id

    class Meta:
        db_table = "position"
        verbose_name = _("PositionModel")
        verbose_name_plural = _("PositionModels")
