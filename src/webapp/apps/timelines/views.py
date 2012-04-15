#coding=utf-8

from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings

from respite import Views
from respite.decorators import override_supported_formats, login_required

from apps.timelines.models import Timeline


class TimelineViews(Views):
    supported_formats = ['html', 'json', 'xml']
    
    @login_required
    def chronology(self, request, page=0):
        """
            RETURN THE CHRONOLOGY OF A USER
        """
        if page is None:
            page = 0
        timelines = request.user.get_chronology()[int(page)*settings.TIMELINE_PAGINATION_PER_PAGE:(int(page)+1)*settings.TIMELINE_PAGINATION_PER_PAGE]
        
        return self._render(
                            request = request,
                            template = 'generic/timeline',
                            context = {
                                       'timelines': timelines,
                                       },
                            status = 200)
    
    def timeline(self, request, username=None, page=0):
        if username is None:
            use = request.user
        else:
            user = User.objects.filter(username=username.lower()).select_related('profile')
            if user:
                user = user[0]
            else:
                return self._notfound(request)
        if page is None:
            page = 0
        if not user.profile.can_view_profile(request.user):
            return self._forbidden(request)
        timelines = Timeline.objects.get_by_user(username)[int(page)*settings.TIMELINE_PAGINATION_PER_PAGE:(int(page)+1)*settings.TIMELINE_PAGINATION_PER_PAGE]
        return self._render(
                            request = request,
                            template = 'generic/timeline',
                            context = {
                                       'timelines': timelines,
                                       },
                            status = 200)

def settings_edit(request):
    pass

def settings_detail(request):
    pass