from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import TutorialModel
from unfold.contrib.forms.widgets import WysiwygWidget, ArrayWidget
from django.db.models import TextField
from django.contrib.postgres.fields import ArrayField


@admin.register(TutorialModel)
class TutorialAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
    search_fields = ["name", "desc"]
    autocomplete_fields = ["users"]
    formfield_overrides = {
        TextField: {"widget": WysiwygWidget},
        ArrayField: {"widget": ArrayWidget},
    }
