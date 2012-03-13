#coding=utf-8


from django.contrib.gis import admin
from models import Place #@UnusedWildImport


class PlaceAdmin(admin.GeoModelAdmin):
    model = Place
    readonly_fields  = ['created', 'modified', 'slug']

admin.site.register(Place, PlaceAdmin)