# coding=utf-8

from django.conf.urls.defaults import *
import ajax_views as timelines_views


urlpatterns = patterns('',
    # Seguir o no
    url(r'^ajax/follower/toggle/$',
       timelines_views.toggle_follower,
       name='ajax_follower_toggle'),
    # Esta siguiendo
    url(r'^ajax/follower/is/$',
       timelines_views.is_follower,
       name='ajax_follower_is'),
    # Obtener seguidores
    url(r'^ajax/follower/get/$',
       timelines_views.get_followers,
       name='ajax_follower_get'),
    
   )