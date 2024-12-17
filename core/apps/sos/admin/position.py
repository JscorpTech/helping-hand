from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import PositionModel
from django.contrib.gis import admin as gisadmin


@admin.register(PositionModel)
class PositionAdmin(ModelAdmin, gisadmin.GISModelAdmin):
    list_display = ("id", "__str__", "location")

    class Media:
        css = {
            "all": ("/resources/static/css/gis.css",)
        }
