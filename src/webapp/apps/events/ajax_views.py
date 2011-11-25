#coding=utf-8

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from libs.decorators import ajax_request
from forms import SuggestionForm
from models import Suggestion
from places.models import Place


@ajax_request
@login_required
def suggestion_add(request):
    """
    Añade o edita una sugerencia
    Parametros en POST:
    eventid: el id del evento a editar (opcional)
    """
    eventid = request.POST.get('eventid', None)
    if eventid is not None:
        suggestion = get_object_or_404(Suggestion, pk=eventid)
        form = SuggestionForm(request.POST, instance=suggestion)
    else:
        form = SuggestionForm(request.POST)
    if form.is_valid():
        poi_id = request.POST.get('poi_id', None)
        place = None
        if poi_id is not None and poi_id != '':
            place = get_object_or_404(Place, pk=poi_id)
        else:
            place_reference = request.POST.get('place_reference', None)
            if place_reference is not None and place_reference != '':
                place = Place.objects.create_from_google(
                                         google_places_reference = place_reference,
                                         user = request.user
                                         )
        suggestion = form.save(user=request.user, place=place)
        return HttpResponse(simplejson.dumps(suggestion), mimetype="application/json")
    return HttpResponseBadRequest(simplejson.dumps(form.errors), mimetype="application/json")


@ajax_request
@login_required
def suggestion_follow(request):
    eventid = request.POST.get('eventid', None)
    if eventid is None:
        return HttpResponseBadRequest('eventid needed')
    suggestion = get_object_or_404(Suggestion, pk=eventid)
    added = Suggestion.objects.toggle_follower(follower = request.user,
                                             suggestion=suggestion)
    if added is None:
        return HttpResponseBadRequest()
    else:
        return HttpResponse(simplejson.dumps(added), mimetype="application/json")
    

@ajax_request
@login_required
def suggestion_delete(request):
    eventid = request.POST.get('eventid', None)
    if eventid is None:
        return HttpResponseBadRequest('eventid needed')
    suggestion = get_object_or_404(Suggestion, pk=eventid)
    if suggestion.user__id != request.user.id:
        raise PermissionDenied
    deleted = suggestion.delete()
    return HttpResponse(simplejson.dumps(deleted), mimetype="application/json")
    

