from django_filters import rest_framework as filters

from ..models import TestModel


class TestFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = TestModel
        fields = ("name",)


class VariantFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = VariantModel
        fields = ("name",)


class QuestionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = QuestionModel
        fields = ("name",)


class AnswerFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = AnswerModel
        fields = ("name",)
