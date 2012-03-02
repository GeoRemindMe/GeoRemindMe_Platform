#coding=utf-8

from django.conf.urls.defaults import *

import views as places_views


urlpatterns = patterns('',
    # Editar place
    url(r'^place/(?P<slug>[\.\w]+)/edit/$',
       places_views.place_edit,
       name='place_place_edit'),
    # Ver place
    url(r'^place/(?P<slug>[^/]+)/$',
       places_views.place_detail,
       name='places_place_detail'),
    # Añadir place
    url(r'^places/add/$',
       places_views.place_add,
       name='places_place_add'),
    # Listar places
    url(r'^places/$',
       places_views.places_list,
       name='places_places_list'),
   )