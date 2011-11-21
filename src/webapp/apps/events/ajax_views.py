#coding=utf-8

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import simplejson

from libs.decorators import ajax_request
from forms import SuggestionForm
from models import Suggestion
from places.models import Place


@ajax_request
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
