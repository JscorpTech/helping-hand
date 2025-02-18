from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import UserRequestModel


@admin.register(UserRequestModel)
class UserrequestAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
