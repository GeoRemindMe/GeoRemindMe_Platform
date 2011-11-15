#coding=utf-8

from django.conf.urls.defaults import *

import views as suggestions_views


urlpatterns = patterns('',
    # Editar sugerencia
    url(r'^suggestion/(?P<slug>[\.\w]+)/edit/$',
       suggestions_views.suggestion_edit,
       name='suggestions_suggestion_edit'),
    # Ver sugerencia
    url(r'^suggestion/(?P<slug>[\.\w]+)/$',
       suggestions_views.suggestion_detail,
       name='suggestions_suggestion_detail'),
    # Añadir sugerencias
    url(r'^suggestions/add/$',
       suggestions_views.suggestion_add,
       name='suggestions_suggestion_add'),
    # Listar sugerencias
    url(r'^suggestions/$',
       suggestions_views.suggestions_list,
       name='suggestions_suggestions_list'),
   )