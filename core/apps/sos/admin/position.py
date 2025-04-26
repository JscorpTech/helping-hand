from django.contrib import admin
from django.contrib.gis import admin as gisadmin
from unfold.admin import ModelAdmin

from ..models import PositionModel


@admin.register(PositionModel)
class PositionAdmin(ModelAdmin, gisadmin.GISModelAdmin):
    list_display = ("id", "__str__", "location")

    class Media:
        css = {"all": ("/resources/static/css/gis.css",)}
