from django.conf.urls.defaults import *

urlpatterns = patterns('taggit.views',
    url(r'^list$', 'list_tags', name='taggit-list'),
)


