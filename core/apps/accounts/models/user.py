from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel

from ..choices import RoleChoice
from ..managers import UserManager


class User(auth_models.AbstractUser):
    phone = models.CharField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    role = models.CharField(
        max_length=255,
        choices=RoleChoice,
        default=RoleChoice.USER,
    )

    updated_at = models.DateTimeField(auto_now=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone"
    objects = UserManager()

    @cached_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.phone


class ModeratorModel(AbstractBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="moderator")
    experience = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.user.full_name

    class Meta:
        db_table = "moderator"
        verbose_name = _("ModeratorModel")
        verbose_name_plural = _("ModeratorModels")
