from django_filters import rest_framework as filters

from ..models import TaskModel


class TaskFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = TaskModel
        fields = ("name",)
