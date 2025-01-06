from django.db import models
from django.utils.translation import gettext_lazy as _


class RoleChoice(models.TextChoices):
    """
    User Role Choice
    """

    SUPERUSER = "superuser", _("Superuser")
    ADMIN = "admin", _("Admin")
    USER = "user", _("User")
    PSIXOLOG = "psixolog", _("Psixolog")
    LAWYER = "lawyer", _("Lawyer")
    BUSINESS = "business", _("Business")

    def moderator_roles() -> list:
        return [
            RoleChoice.LAWYER,
            RoleChoice.PSIXOLOG,
            RoleChoice.BUSINESS,
        ]

    def moderator_tuple() -> list:
        return [
            (RoleChoice.LAWYER.value, RoleChoice.LAWYER.label),
            (RoleChoice.PSIXOLOG.value, RoleChoice.PSIXOLOG.label),
            (RoleChoice.BUSINESS.value, RoleChoice.BUSINESS.label),
        ]


class AuthProviderChoice(models.TextChoices):
    """
    User Role Choice
    """

    PHONE = "phone", _("Phone")
    GOOGLE = "google", _("Google")
