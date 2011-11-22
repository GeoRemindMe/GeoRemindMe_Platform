#coding=utf-8

from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from models import Suggestion, EventFollower
from profiles.models import User


@login_required
def suggestions_user(request, username):
    if username != request.user.username:
        try:
            user = User.objects.select_related('profile').get(
                                                      username__iexact=username
                                                      )
        except User.DoesNotExist:
            raise Http404
        if not user.profile.can_view_profile(request.user):
            return HttpResponseForbidden(_("No tienes permiso para ver este perfil"))
        follower = user
    else:
        follower = request.user
    suggestions = Suggestion.objects.get_suggestions_by_follower(follower=follower)
    return HttpResponse(','.join(s.__unicode__() for s in suggestions))


@login_required
def suggestion_edit(request, slug):
    suggestion = get_object_or_404(Suggestion, 
                                   user = request.user,
                                   slug__iexact = slug)
    
    return render_to_response('events/suggestion_edit.html', 
                              {'suggestion': suggestion},
                              context_instance = RequestContext(request))


def suggestion_detail(request, slug):
    try:
        suggestion = Suggestion.objects.select_related(
                                                       'user', 
                                                       'place', 
                                                       'place__city', 
                                                       'place__city__region',
                                                       'place__city__region__country',
                                                       ).get(slug__iexact=slug)
    except Suggestion.DoesNotExist:
        raise Http404
    if not suggestion._is_public() and suggestion.user_id != request.user.id:
        return HttpResponseForbidden(_(u"No puedes ver esta sugerencia"))
    return render_to_response('events/suggestion_detail.html',
                              {'suggestion': suggestion},
                              context_instance = RequestContext(request))


@login_required
def suggestion_add(request):
    return render_to_response('events/suggestion_add.html', 
                              {},
                              context_instance = RequestContext(request))


def suggestions_list(request):
    pass
