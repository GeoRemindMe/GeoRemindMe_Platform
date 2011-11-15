#coding=utf-8

from django.conf.urls.defaults import *

import views as places_views


urlpatterns = patterns('',
    # Editar place
    url(r'^place/(?P<slug>[\.\w]+)/edit/$',
       places_views.place_edit,
       name='place_place_edit'),
    # Ver sugerencia
    url(r'^place/(?P<slug>[\.\w]+)/$',
       places_views.place_detail,
       name='places_place_detail'),
    # Añadir sugerencias
    url(r'^place/add/$',
       places_views.place_add,
       name='places_place_add'),
    # Listar sugerencias
    url(r'^suggestions/$',
       places_views.places_list,
       name='places_places_list'),
   )