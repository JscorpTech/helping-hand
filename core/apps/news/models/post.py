from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class PostModel(AbstractBaseModel):
    title = models.CharField(_("title"), max_length=255)
    content = models.TextField(_("content"))
    image = models.ImageField(_("image"), upload_to="news/")

    @classmethod
    def _create_face(self):
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
