from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class BannerModel(AbstractBaseModel):
    title = models.CharField(_("name"), max_length=255)
    subtitle = models.CharField(_("subtitle"), max_length=255)
    color_right = models.CharField(_("color right"), max_length=255, default="#000000")
    color_left = models.CharField(_("color left"), max_length=255, default="#000000")
    image = models.ImageField(_("image"), upload_to="banners/")
    link = models.CharField(_("link"), max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            title="Test",
            subtitle="Test",
            color_right="#000000",
            color_left="#000000",
            link="news",
        )

    class Meta:
        db_table = "banner"
        verbose_name = _("BannerModel")
        verbose_name_plural = _("BannerModels")
