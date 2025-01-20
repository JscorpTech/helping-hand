from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import ExamModel, ExamResultModel, SertificateModel
from unfold.decorators import display
from ..choices import SertificateChoices
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import ChoicesDropdownFilter

@admin.register(ExamModel)
class ExamAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(SertificateModel)
class SertificateAdmin(ModelAdmin):
    list_display = ("id", "__str__", "_status")
    list_filter = [("status", ChoicesDropdownFilter)]
    list_filter_submit = True

    @display(
        description=_("Status"),
        ordering="status",
        label={
            SertificateChoices.ACTIVE.label: "success",
            SertificateChoices.INACTIVE.label: "danger",
            SertificateChoices.DRAFT.label: "warning",
        },
    )
    def _status(self, obj):
        return obj.get_status_display()


@admin.register(ExamResultModel)
class ExamresultAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
