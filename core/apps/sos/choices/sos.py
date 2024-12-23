from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class AreaChoice(TextChoices):
    """Xafli hudud — Dangerous area
    Xafsiz hudud — Unsafe area"""

    DANGEROUS = "dangerous", _("Xafli hudud")
    UNSAFE = "unsafe", _("Xafsiz hudud")
