from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel

class FaqModel(AbstractBaseModel):
    question=models.TextField(_("question"),)
    answer=models.TextField(_("answer"))
    updated_date=models.DateTimeField(_("updated date"),auto_now=True)
    created_date=models.DateTimeField(_("created date"),auto_now_add=True)
    
    def __str__(self):
        return self.question

    @classmethod
    def _create_fake(self):
        return self.objects.create(
            question="Test?",
            answer="TEST"
        )
    

    class Meta:
        db_table="faq"
        verbose_name=_("FAQModel")
        verbose_name_plural=_("FAQModels")