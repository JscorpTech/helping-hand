from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from ..choices import TutorialTypeChoice


class TutorialModel(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255)
    desc = models.TextField(_("description"), blank=True, null=True)
    image = models.ImageField(_("banner"), upload_to="tutorials/")
    file = models.FileField(_("file"), upload_to="tutorials/", blank=True, null=True)
    video = models.FileField(_("video"), upload_to="tutorials/", blank=True, null=True)
    test = models.ForeignKey(
        "TestModel", verbose_name=_("test"), on_delete=models.CASCADE, related_name="tutorials", blank=True, null=True
    )
    task = models.ForeignKey(
        "TaskModel", verbose_name=_("task"), on_delete=models.CASCADE, related_name="tutorials", blank=True, null=True
    )
    tags = ArrayField(verbose_name=_("tags"), blank=True, null=True, base_field=models.CharField(max_length=255))
    position = models.PositiveIntegerField(_("position"), default=0)
    source = models.URLField(_("source"), blank=True, null=True)
    tutorial_type = models.CharField(
        _("type"), choices=TutorialTypeChoice.choices, max_length=255, default=TutorialTypeChoice.LAWYER
    )
    users = models.ManyToManyField(
        verbose_name=_("users"),
        to=get_user_model(),
        related_name="tutorials",
        blank=True,
    )

    @classmethod
    def _create_fake(cls):
        return cls.objects.create(
            name="Test",
            desc="Test",
            image="image.jpg",
            file="file.zip",
            video="video.mp4",
            tags=[],
            tutorial_type=TutorialTypeChoice.LAWYER,
            position=1,
            source="http://example.com",
        )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tutorial"
        verbose_name = _("TutorialModel")
        verbose_name_plural = _("TutorialModels")
