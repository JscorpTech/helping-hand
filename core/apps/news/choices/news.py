from django.db import models
from django.utils.translation import gettext_lazy as _


class NewsTypeChoice(models.TextChoices):
    PSIXOLOG = "psixolog", _("Psixolog")
    LAWYER = "lawyer", _("Lawyer")
    BUSINESS = "business", _("Business")

    @property
    def tuple():
        return [
            (NewsTypeChoice.LAWYER.value, NewsTypeChoice.LAWYER.label),
            (NewsTypeChoice.PSIXOLOG.value, NewsTypeChoice.PSIXOLOG.label),
            (NewsTypeChoice.BUSINESS.value, NewsTypeChoice.BUSINESS.label),
        ]
