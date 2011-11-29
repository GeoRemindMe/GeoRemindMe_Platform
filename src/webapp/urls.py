from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': ('webapp',),
}

from events.models import *


urlpatterns = patterns('',
   url(r'', include('profiles.urls')), # perfiles
   url(r'', include('mainApp.urls')), # aplicacion principal
   url(r'', include('timelines.urls')), # notificaciones timeline
   url(r'', include('places.urls')), # places
   url(r'', include('events.urls')), # events
   url(r'', include('lists.urls')), # events
   url(r'ajax/', include('timelines.ajax_urls')), # timelines AJAX
   url(r'ajax/', include('profiles.ajax_urls')), # profiles AJAX
   url(r'ajax/', include('events.ajax_urls')), # events AJAX
   url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict, 'jsi18n'), # i18n para javascript
   #url(r'^accounts/', include('userena.urls')), # userena
   url(r'^messages/', include('userena.contrib.umessages.urls')), # framework de mensajes de userena
   url(r'^social/', include('socialregistration.urls',namespace = 'socialregistration')), # socialregistration
   url(r'^sentry/', include('sentry.web.urls')),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^admin_tools/', include('admin_tools.urls')),
   url(r'^translations/', include('datatrans.urls')),
)
