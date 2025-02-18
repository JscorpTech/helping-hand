from django.db import models
from django.utils.translation import gettext_lazy as _


class TutorialTypeChoice(models.TextChoices):
    PSIXOLOG = "psixolog", _("Psixolog")
    LAWYER = "lawyer", _("Lawyer")
    BUSINESS = "business", _("Business")
    DOCUMENT = "document", _("Document")

    @property
    def tuple():
        return [
            (TutorialTypeChoice.LAWYER.value, TutorialTypeChoice.LAWYER.label),
            (TutorialTypeChoice.PSIXOLOG.value, TutorialTypeChoice.PSIXOLOG.label),
            (TutorialTypeChoice.BUSINESS.value, TutorialTypeChoice.BUSINESS.label),
            (TutorialTypeChoice.DOCUMENT.value, TutorialTypeChoice.DOCUMENT.label),
        ]
