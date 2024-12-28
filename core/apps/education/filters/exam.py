from django_filters import rest_framework as filters

from ..models import ExamModel, ExamResultModel, SertificateModel


class ExamFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ExamModel
        fields = ("name",)


class SertificateFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = SertificateModel
        fields = ("name",)


class ExamresultFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ExamResultModel
        fields = ("name",)
