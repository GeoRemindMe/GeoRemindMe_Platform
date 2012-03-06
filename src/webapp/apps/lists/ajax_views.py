coding=utf-8

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.core import serializers

from libs.decorators import ajax_request
from forms import ListSuggestionForm
from models import ListSuggestion
from places.models import Place


@ajax_request
@login_required
def listsuggestion_add(request):
    """
    Cra una lista de sugerencias o modifica una
    si se especifica id
    Parametros en POST:
    list_id: id de la lista (opcional)
    name: nombre de la lista (unico por usuario)
    description: descripcion (opcional)
    suggestions: lista de ids de sugerencias
    """
    listid = request.POST.get('listid', None)
    list_instances = request.POST.getlist('suggestions[]')
    list_instances_del = request.POST.getlist('suggestions_del[]')
    if listid is not None:
        listsuggestion = get_object_or_404(ListSuggestion, pk=listid)
        form = ListSuggestionForm(request.POST, instance=listsuggestion)
    else:
        form = ListSuggestionForm(request.POST)
    if form.is_valid():
        listobj = form.save(user=request.user, ids = list_instances, ids_del=list_instances_del)
        if listobj is not None:
            json_serializer = serializers.get_serializer("json")()
            data = json_serializer.serialize([listobj], ensure_ascii=False)
            return HttpResponse(data, mimetype="application/json")
    else:
        return HttpResponseBadRequest(simplejson.dumps(form.errors), mimetype="application/json")
    return HttpResponseBadRequest()
