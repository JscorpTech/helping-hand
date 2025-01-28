from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters import rest_framework as filters

from core.apps.accounts.choices import RoleChoice


class ModeratorFilter(filters.FilterSet):
    role = filters.ChoiceFilter(
        field_name="role",
        choices=RoleChoice.moderator_tuple(),
    )

    search = filters.CharFilter(
        method="filter_by_name",
        label="Search by first or last name",
    )

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value))

    class Meta:
        model = get_user_model()
        fields = (
            "role",
            "search",
        )
