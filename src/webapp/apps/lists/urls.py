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
   )