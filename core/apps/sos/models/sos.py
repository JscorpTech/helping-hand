from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel

from ..choices import AreaChoice


class UserRequestModel(AbstractBaseModel):
    user = models.ForeignKey(
        verbose_name=_("user"), to=get_user_model(), on_delete=models.CASCADE, related_name="sos_requests"
    )
    area = models.CharField(_("area"), choices=AreaChoice.choices, max_length=255)

    def __str__(self):
        return self.user.full_name

    class Meta:
        db_table = "user_request"
        verbose_name = _("UserrequestModel")
        verbose_name_plural = _("UserrequestModels")
