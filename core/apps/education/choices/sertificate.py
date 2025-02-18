from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class SertificateChoices(TextChoices):
    ACTIVE = "active", _("Active")
    INACTIVE = "inactive", _("Inactive")
    DRAFT = "draft", _("Draft")
