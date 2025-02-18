from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel


class FaqCategoryModel(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def _create_fake(self):
        return self.objects.create(name="Test")

    class Meta:
        db_table = "faq_category"
        verbose_name = _("FaqCategoryModel")
        verbose_name_plural = _("FaqCategoryModels")


class FaqModel(AbstractBaseModel):
    category = models.ForeignKey(
        FaqCategoryModel, on_delete=models.CASCADE, related_name="questions", verbose_name=_("category")
    )
    question = models.TextField(_("question"))
    answer = models.TextField(_("answer"))

    def __str__(self):
        return self.question

    # @classmethod
    # def _create_fake(self):
    #     return self.objects.create(question="Test?", answer="TEST")

    class Meta:
        db_table = "faq"
        verbose_name = _("FAQModel")
        verbose_name_plural = _("FAQModels")
