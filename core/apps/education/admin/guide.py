from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import GuideModel
from unfold.contrib.forms.widgets import WysiwygWidget
from django.db.models import TextField
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(GuideModel)
class GuideAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "__str__",
    )
    formfield_overrides = {
        TextField: {"widget": WysiwygWidget},
    }
