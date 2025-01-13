from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from django.utils.functional import cached_property

from ..choices import ChatTypeChoice, FileTypeChoice
from typing import Union


class GroupModel(AbstractBaseModel):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("name"))
    is_public = models.BooleanField(_("is:public"), default=False)
    image = models.ImageField(_("image"), upload_to="groups/", blank=True, null=True)
    chat_type = models.CharField(_("chat type"), choices=ChatTypeChoice.choices, null=True, blank=True)
    users = models.ManyToManyField(verbose_name=_("users"), to=get_user_model(), related_name="chats", blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_user(self, user, group):
        obj_type, obj = group.user(user, group)
        if obj_type == "group":
            return None
        return obj

    @classmethod
    def chat_name(self, user, group):
        obj_type, obj = group.user(user, group)
        if obj_type == "group":
            return group.name
        return obj.full_name

    @classmethod
    def user(self, user, group) -> list:
        if group.is_public:
            return "group", group
        users = group.users.exclude(id=user.id)
        if users.exists():
            return "user", users.first()
        return "group", group

    def _chat_image(user, group) -> Union[str, None]:
        obj_type, obj = group.user(user, group)
        if obj_type == "group":
            return group.image
        return obj.avatar

    @classmethod
    def chat_image(self, user, group, request):
        try:
            image = self._chat_image(user, group)
        except:
            return None
        if not image:
            return None
        return request.build_absolute_uri(image.url)

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
            is_public=True,
            chat_type=ChatTypeChoice.LAWYER,
        )

    @cached_property
    def members(self):
        return self.users.all()

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
    is_read = models.BooleanField(verbose_name=_("is read"), default=False)
    file_type = models.CharField(
        verbose_name=_("file type"), max_length=50, null=True, blank=True, choices=FileTypeChoice.choices
    )
    group = models.ForeignKey(
        verbose_name=_("group"), to="GroupModel", on_delete=models.CASCADE, related_name="messages"
    )
    user = models.ForeignKey(verbose_name=_("user"), to=get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        db_table = "message"
        verbose_name = _("MessageModel")
        verbose_name_plural = _("MessageModels")
