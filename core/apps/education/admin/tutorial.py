from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import TutorialModel


@admin.register(TutorialModel)
class TutorialAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
    search_fields = ["name", "desc"]
    autocomplete_fields = ["users"]
