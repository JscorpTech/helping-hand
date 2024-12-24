from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from core.apps.accounts.choices import RoleChoice


class ModeratorFilter(filters.FilterSet):
    role = filters.ChoiceFilter(
        field_name="role",
        choices=RoleChoice.moderator_tuple(),
    )

    class Meta:
        model = get_user_model()
        fields = ("role",)
