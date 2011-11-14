# coding=utf-8

from django.conf.urls.defaults import *

import views as timelines_views


urlpatterns = patterns('',
    # Editar perfil
    url(r'^settings/edit/$',
       timelines_views.settings_edit,
       name='timelines_settings_edit'),
    # Ver perfil
    url(r'^settings/$',
       timelines_views.settings_detail,
       name='timelines_settings_detail'),
   )