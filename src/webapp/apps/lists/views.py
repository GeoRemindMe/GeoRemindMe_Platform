#coding=utf-8

from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from models import ListSuggestion
from profiles.models import User



@login_required
def listsuggestion_edit(request, id):
    listobj = get_object_or_404(ListSuggestion, 
                                       user = request.user,
                                       id = id)
    
    return render_to_response('lists/listsuggestion_edit.html', 
                              {'list': listobj},
                              context_instance = RequestContext(request))


def listsuggestion_detail(request, id):
    try:
        listobj = ListSuggestion.objects.select_related(
                                                       'user',
                                                       'suggestions'
                                                       'place', 
                                                       'place__city', 
                                                       'place__city__region',
                                                       'place__city__region__country',
                                                       ).get(id=id)
    except ListSuggestion.DoesNotExist:
        raise Http404
    if not listobj._is_public() and listobj.user_id != request.user.id:
        return HttpResponseForbidden(_(u"No puedes ver esta sugerencia"))
    return render_to_response('lists/listsuggestion_detail.html',
                              {'list': listobj},
                              context_instance = RequestContext(request))


@login_required
def suggestion_add(request):
    return render_to_response('events/suggestion_add.html', 
                              {},
                              context_instance = RequestContext(request))


def suggestions_list(request):
    pass
