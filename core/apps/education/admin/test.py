from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from ..models import QuestionModel, ResultModel, TestModel, VariantModel
from unfold.contrib.forms.widgets import WysiwygWidget
from django.db.models import TextField
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline


class VariantInline(TabularInline, TranslationTabularInline):
    model = VariantModel
    extra = 1
    tab = True


class QuestionInline(TabularInline, TranslationTabularInline):
    model = QuestionModel
    extra = 1


@admin.register(TestModel)
class TestAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "__str__",
    )

    inlines = [QuestionInline]

    search_fields = ["topic", "desc"]


@admin.register(VariantModel)
class VariantAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "__str__",
        "is_true",
        "question"
    )


@admin.register(QuestionModel)
class QuestionAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "__str__",
    )
    search_fields = ["question"]
    inlines = [VariantInline]

    formfield_overrides = {
        TextField: {"widget": WysiwygWidget},
    }


@admin.register(ResultModel)
class ResultAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
