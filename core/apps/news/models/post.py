from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from ..choices import NewsTypeChoice


class PostModel(AbstractBaseModel):
    title = models.CharField(_("title"), max_length=255)
    content = models.TextField(_("content"))
    image = models.ImageField(_("image"), upload_to="news/")
    is_top = models.BooleanField(_("is top"), default=False)
    views = models.BigIntegerField(_("views"), default=0)
    news_type = models.CharField(
        _("type"), choices=NewsTypeChoice.choices, max_length=255, default=NewsTypeChoice.BUSINESS
    )

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            title="Test",
            content="Test",
            image="image.jpg",
        )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "post"
        verbose_name = _("PostModel")
        verbose_name_plural = _("PostModels")
