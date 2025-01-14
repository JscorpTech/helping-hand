from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from django.utils.functional import cached_property

from ..choices import ChatTypeChoice, FileTypeChoice


class GroupModel(AbstractBaseModel):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("name"))
    is_public = models.BooleanField(_("is:public"), default=False)
    image = models.ImageField(_("image"), upload_to="groups/", blank=True, null=True)
    chat_type = models.CharField(_("chat type"), choices=ChatTypeChoice.choices, null=True, blank=True)
    users = models.ManyToManyField(verbose_name=_("users"), to=get_user_model(), related_name="chats", blank=True)

    def __str__(self):
        return self.name

    def get_chat_details(self, user):
        """Foydalanuvchiga tegishli chat tafsilotlarini qaytaradi."""
        if self.is_public:
            return {"type": "group", "name": self.name, "image": self.image}
        other_users = self.users.exclude(id=user.id)
        if other_users.exists():
            other_user = other_users.first()
            return {"type": "user", "id": other_user.id, "name": other_user.full_name, "image": other_user.avatar}
        return {"type": "group", "name": self.name, "image": self.image}

    def chat_image(self, user, request):
        details = self.get_chat_details(user)
        image = details.get("image")
        if image:
            return request.build_absolute_uri(image.url)
        return None

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            name="Test",
            is_public=True,
            chat_type=ChatTypeChoice.LAWYER,
        )

    def new_message_count(self, user) -> int:
        """Yeni xabarlar sonini qaytaradi."""
        return self.messages.filter(is_read=False).exclude(user__in=[user]).count()

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
