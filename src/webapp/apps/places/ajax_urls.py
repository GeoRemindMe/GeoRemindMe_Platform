#coding=utf-8

from django.conf.urls.defaults import *
import ajax_views as events_views


urlpatterns = patterns('',
    # Nuevo place
    url(r'^ajax/place/add/$',
       events_views.place_add,
       name='ajax_place_add'),
    # Esta siguiendo
    url(r'^ajax/place/(?P<slug>[\.\w]+)/$',
       events_views.place_details,
       name='ajax_place_detail'),
   )