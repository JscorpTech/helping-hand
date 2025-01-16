from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import ExamModel, ExamResultModel, SertificateModel


@admin.register(ExamModel)
class ExamAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(SertificateModel)
class SertificateAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(ExamResultModel)
class ExamresultAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
