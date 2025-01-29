import django_filters
from ..models import FaqModel, FaqCategoryModel


class FaqModelFilter(django_filters.FilterSet):
    question = django_filters.CharFilter(lookup_expr="icontains")
    answer = django_filters.CharFilter(lookup_expr="icontains")
    category = django_filters.NumberFilter(field_name="category__id", lookup_expr="exact")
    created_at = django_filters.DateFilter(field_name="created_at", lookup_expr="exact")

    class Meta:
        model = FaqModel
        fields = ["question", "answer", "category", "created_at"]


class FaqCategoryModelFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    created_at = django_filters.DateFilter(field_name="date_created", lookup_expr="exact")

    class Meta:
        model = FaqCategoryModel
        fields = ["name", "created_at"]
