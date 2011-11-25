#coding=utf-8


from django.contrib.gis import admin
from django.contrib.gis.maps.google import GoogleMap
from django.conf import settings
from models import * #@UnusedWildImport


GMAP = GoogleMap(key=settings.GOOGLE_API_PASSWORD['google_maps_secure'], version='3')

class GoogleAdmin(admin.ModelAdmin):#.options.OSMGeoAdmin):
    extra_js = [GMAP.api_url + GMAP.key]
    map_template = 'gis/admin/google.html'
    search_fields = ['name']


admin.site.register(Place, admin.GeoModelAdmin)
