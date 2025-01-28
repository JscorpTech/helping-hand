from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db.models import TextField
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget

from ..models import TutorialModel


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
