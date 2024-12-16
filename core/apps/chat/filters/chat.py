from django_filters import rest_framework as filters

from ..models import GroupModel


class ContentFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = GroupModel
        fields = ("name",)


class ContentFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = MessageModel
        fields = ("name",)
