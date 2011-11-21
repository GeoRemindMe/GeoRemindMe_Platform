#coding=utf-8

from django.conf.urls.defaults import *
import ajax_views as timelines_views


urlpatterns = patterns('',
    # Seguir o no
    url(r'^follower/toggle/$',
       timelines_views.toggle_follower,
       name='timelines_follower_toggle'),
    # Esta siguiendo
    url(r'^follower/is/$',
       timelines_views.is_follower,
       name='timelines_follower_is'),
    # Obtener seguidores
    url(r'^follower/get/$',
       timelines_views.get_followers,
       name='timelines_follower_get'),
    
   )