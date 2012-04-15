#coding=utf-8

from django.conf.urls.defaults import *
from respite.urls import resource, routes, templates

from views import *


urlpatterns = resource(
    prefix = '',
    views = TimelineViews,
    routes = [
        # Route to backpack
        routes.route(
            regex = r'^chronology(?:\.[a-zA-Z]+)?(?:/(?P<page>[0-9]+))?/$',
            view = 'chronology',
            method = 'GET',
            name = 'timeline_chronology_user'
        ),
        routes.route(
            regex = r'^timeline(?:\.[a-zA-Z]+)?(?:/(?P<page>[0-9]+))?/$',
            view = 'timeline',
            method = 'GET',
            name = 'timeline_user'
        ),
        routes.route(
            regex = r'^timeline(?:\.[a-zA-Z]+)?/(?P<username>[^/]+)(?:/(?P<page>[0-9]+))?/$',
            view = 'timeline',
            method = 'GET',
            name = 'timeline_user'
        ),
      ]
)
#
#import views as timelines_views
#
#
#urlpatterns = patterns('',
#    # Editar perfil
#    url(r'^settings/edit/$',
#       timelines_views.settings_edit,
#       name='timelines_settings_edit'),
#    # Ver perfil
#    url(r'^settings/$',
#       timelines_views.settings_detail,
#       name='timelines_settings_detail'),
#   )