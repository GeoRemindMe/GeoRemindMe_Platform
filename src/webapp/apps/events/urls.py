#coding=utf-8

from django.conf.urls.defaults import *

import views as suggestions_views


urlpatterns = patterns('',
    # mochila
    url(r'^!/(?P<username>[\.\w]+)/suggestions/$',
       suggestions_views.suggestions_user,
       name='events_suggestions_user'),
    # Ver sugerencia
    url(r'^suggestion/(?P<slug>[-\w]+)/$',
       suggestions_views.suggestion_detail,
       name='events_suggestion_detail'),
    # Editar sugerencia
    url(r'^suggestion/(?P<slug>[^/]+)/edit/$',
       suggestions_views.suggestion_edit,
       name='events_suggestion_edit'),
    # Añadir sugerencias
    url(r'^suggestions/add/$',
       suggestions_views.suggestion_add,
       name='events_suggestion_add'),
    # Listar sugerencias
    url(r'^suggestions/$',
       suggestions_views.suggestions_list,
       name='events_suggestions_list'),
   )