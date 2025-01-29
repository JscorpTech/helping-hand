from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from ..models import TaskModel, TaskResultModel


@admin.register(TaskModel)
class TaskAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(TaskResultModel)
class TaskResultAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
