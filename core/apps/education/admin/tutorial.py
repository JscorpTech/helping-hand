from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import TutorialModel
from unfold.contrib.forms.widgets import WysiwygWidget, ArrayWidget
from django.db.models import TextField
from django.contrib.postgres.fields import ArrayField
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(TutorialModel)
class TutorialAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "__str__",
    )
    search_fields = ["name_uz", "name_kaa", "name_kril", "desc"]
    autocomplete_fields = ["users"]
    formfield_overrides = {
        TextField: {"widget": WysiwygWidget},
        ArrayField: {"widget": ArrayWidget},
    }
