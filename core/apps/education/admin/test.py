from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from ..models import AnswerModel, QuestionModel, TestModel, VariantModel


class VariantInline(TabularInline):
    model = VariantModel
    extra = 1
    tab = True


class QuestionInline(TabularInline):
    model = QuestionModel
    extra = 1


@admin.register(TestModel)
class TestAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )

    inlines = [QuestionInline]

    autocomplete_fields = ["questions"]
    search_fields = ["topic", "desc"]


@admin.register(VariantModel)
class VariantAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(QuestionModel)
class QuestionAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
    search_fields = ["question"]
    inlines = [VariantInline]


@admin.register(AnswerModel)
class AnswerAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
