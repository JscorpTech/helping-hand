from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import GroupModel, MessageModel


@admin.register(GroupModel)
class GroupAdmin(ModelAdmin):
    list_display = ("id", "__str__", "is_public")
    autocomplete_fields = ["users"]


@admin.register(MessageModel)
class MessageAdmin(ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("group")

    list_display = (
        "id",
        "__str__",
        "group__name",
        "created_at",
        "updated_at",
    )
