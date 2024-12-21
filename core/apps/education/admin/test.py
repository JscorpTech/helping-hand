from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import AnswerModel, QuestionModel, TestModel, VariantModel


@admin.register(TestModel)
class TestAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


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


@admin.register(AnswerModel)
class AnswerAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
