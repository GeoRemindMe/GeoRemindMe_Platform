#coding=utf-8

from django.conf.urls.defaults import *

import ajax_views as profiles_views

urlpatterns = patterns('',
    # Ver dashboard
    url(r'^login/$',
       profiles_views.login,
       name='profiles_login'),
   url(r'^register/$',
       profiles_views.register,
       name='profiles_register'),
   )