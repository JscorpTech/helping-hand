from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class TutorialTypeChoice(TextChoices):
    MANUAL = "manual", _("Manual")
    VIDEO = "video", _("Video")
