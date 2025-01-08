from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from ..models import AnswerModel, QuestionModel, ResultModel, TestModel, VariantModel
from unfold.contrib.forms.widgets import WysiwygWidget
from django.db.models import TextField


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

    formfield_overrides = {
        TextField: {"widget": WysiwygWidget},
    }


@admin.register(AnswerModel)
class AnswerAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(ResultModel)
class ResultAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
