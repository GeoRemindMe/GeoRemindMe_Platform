#coding=utf-8


from django.contrib.gis import admin
from models import * #@UnusedWildImport


admin.site.register(Place, admin.GeoModelAdmin)