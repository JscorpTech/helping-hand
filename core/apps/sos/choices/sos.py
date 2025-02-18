from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class AreaChoice(TextChoices):
    """Xafli hudud — unsafe
    Xafsiz hudud — safe"""

    UNSAFE = "unsafe", _("Xafli hudud")
    SAFE = "safe", _("Xafsiz hudud")
