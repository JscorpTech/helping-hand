from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import GroupModel, MessageModel


@admin.register(GroupModel)
class GroupAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(MessageModel)
class MessageAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
        "created_at",
        "updated_at"
    )
