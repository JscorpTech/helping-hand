from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel

from ..choices import TutorialTypeChoice


class GuideModel(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255)
    desc = models.TextField(_("description"), blank=True, null=True)
    image = models.ImageField(_("banner"), upload_to="guides/")
    file = models.FileField(_("file"), upload_to="guides/", blank=True, null=True)
    video = models.FileField(_("video"), upload_to="guides/", blank=True, null=True)
    guide_type = models.CharField(_("type"), choices=TutorialTypeChoice.choices, max_length=255)
    source = models.URLField(_("source"), blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def _create_fake(cls):
        return cls.objects.create(
            name="Test",  # name of the guide
            desc="test",  # description of the guide
            image="guide.jpg",  # image of the guide
            file="guide.pdf",  # file of the guide
            video="guide.mp4",  # video of the guide
            source="https://example.com",
        )

    class Meta:
        db_table = "guide"
        verbose_name = _("GuideModel")
        verbose_name_plural = _("GuideModels")
