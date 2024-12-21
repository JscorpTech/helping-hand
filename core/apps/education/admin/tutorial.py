from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import TutorialModel


@admin.register(TutorialModel)
class TutorialAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
