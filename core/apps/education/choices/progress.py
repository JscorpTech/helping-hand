from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ProgressChoices(TextChoices):
    NOT_STARTED = "not_started", _("Not started")
    IN_PROGRESS = "in_progress", _("In progress")
    COMPLETED = "completed", _("Completed")
