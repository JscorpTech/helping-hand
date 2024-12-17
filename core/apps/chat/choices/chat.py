from django.db import models
from django.utils.translation import gettext_lazy as _


class ChatTypeChoice(models.TextChoices):
    LAWYER = "lawyer", _("Lawyer")
    PSIXOLOG = "psixolog", _("Psixolog")
