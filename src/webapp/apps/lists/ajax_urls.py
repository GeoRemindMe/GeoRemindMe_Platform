#coding=utf-8

from django.conf.urls.defaults import *

import ajax_views as lists_views

urlpatterns = patterns('',
    # Ver dashboard
    url(r'^ls/add/$',
       lists_views.listsuggestion_add,
       name='lists_suggestion_add_ajax'),
   )