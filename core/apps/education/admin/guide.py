from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import GuideModel


@admin.register(GuideModel)
class GuideAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
