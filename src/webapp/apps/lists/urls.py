#coding=utf-8

from django.conf.urls.defaults import *

import views as list_views


urlpatterns = patterns('',
    # Editar list
    url(r'^ls/(?P<id>[^/]+)/edit/$',
       list_views.listsuggestion_edit,
       name='lists_suggestion_edit'),
    # Ver lista sugerencia
    url(r'^ls/(?P<id>[^/]+)/$',
       list_views.listsuggestion_detail,
       name='lists_suggestion_detail'),
    # Añadir sugerencias
    url(r'^suggestions/add/$',
       list_views.suggestion_add,
       name='events_suggestion_add'),
    # Listar sugerencias
    url(r'^suggestions/$',
       list_views.suggestions_list,
       name='events_suggestions_list'),
   )