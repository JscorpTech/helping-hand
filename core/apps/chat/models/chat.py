from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel

from ..choices import ChatTypeChoice, FileTypeChoice


class GroupModel(AbstractBaseModel):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("name"))
    is_public = models.BooleanField(_("is:public"), default=False)
    image = models.ImageField(_("image"), upload_to="groups/", blank=True, null=True)
    chat_type = models.CharField(_("chat type"), choices=ChatTypeChoice.choices, null=True, blank=True)
    users = models.ManyToManyField(verbose_name=_("users"), to=get_user_model(), related_name="chats", blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
            is_public=True,
            chat_type=ChatTypeChoice.LAWYER,
        )

    class Meta:
        db_table = "group"
        verbose_name = _("GroupModel")
        verbose_name_plural = _("GroupModels")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["chat_type"]),
        ]


class MessageModel(AbstractBaseModel):
    text = models.CharField(verbose_name=_("text"), max_length=500, null=True, blank=True)
    file = models.FileField(verbose_name=_("file"), upload_to="message/", null=True, blank=True)
    file_type = models.CharField(
        verbose_name=_("file type"), max_length=50, null=True, blank=True, choices=FileTypeChoice.choices
    )
    group = models.ForeignKey(verbose_name=_("group"), to="GroupModel", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name=_("user"), to=get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        db_table = "message"
        verbose_name = _("MessageModel")
        verbose_name_plural = _("MessageModels")
