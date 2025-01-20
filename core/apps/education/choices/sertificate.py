from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices


class SertificateChoices(TextChoices):
    ACTIVE = "active", _("Active")
    INACTIVE = "inactive", _("Inactive")
    DRAFT = "draft", _("Draft")
