#coding=utf-8

from django.conf.urls.defaults import *

import ajax_views as events_views

urlpatterns = patterns('',
    # Ver dashboard
    url(r'^suggestion/add/$',
       events_views.suggestion_add,
       name='events_suggestion_add_ajax'),
   )