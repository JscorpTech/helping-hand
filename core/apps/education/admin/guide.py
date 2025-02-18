from django.contrib import admin
from django.db.models import TextField
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from ..models import GuideModel


@admin.register(GuideModel)
class GuideAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "__str__",
    )
    formfield_overrides = {
        TextField: {"widget": WysiwygWidget},
    }
