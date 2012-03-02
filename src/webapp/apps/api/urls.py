#coding=utf-8

from jsonrpc import jsonrpc_site
from django.conf.urls.defaults import *
import apps.api.views

urlpatterns = patterns('',
                       url(r'^browse/$', 
                           'jsonrpc.views.browse',
                           name='jsonrpc_browser'),
                       url(r'^1/', 
                           jsonrpc_site.dispatch, 
                           name='jsonrpc_mountpoint'),
                       
)