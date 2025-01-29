from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class NotificationModel(AbstractBaseModel):
    title = models.CharField(_("title"), max_length=255)
    body = models.TextField(_("body"), null=True, blank=True)
    users = models.ManyToManyField(
        get_user_model(),
        blank=True,
        through="UserNotificationModel",
        through_fields=("notification", "user"),
        related_name="notifications",
        verbose_name=_("users"),
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "notification"
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ["-created_at"]


class UserNotificationModel(AbstractBaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_notifications")
    notification = models.ForeignKey(NotificationModel, on_delete=models.CASCADE, related_name="user_notifications")
    is_read = models.BooleanField(
        _("is read"),
        default=False,
    )
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)

    def __str__(self):
        return self.user.full_name

    class Meta:
        db_table = "user_notification"
        verbose_name = _("User Notification")
        verbose_name_plural = _("User Notifications")
        ordering = ["-created_at"]
