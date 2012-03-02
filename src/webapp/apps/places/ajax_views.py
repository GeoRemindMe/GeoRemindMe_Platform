#coding=utf-8

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import simplejson

from libs.decorators import ajax_request
from models import Place, City, Region, Country


@ajax_request
@login_required
def place_add(request):
    pass


@ajax_request
def place_details(request, slug):
    place = get_object_or_404(Place, slug__iexact=slug)
    return HttpResponse(simplejson.dumps(place), mimetype='application/json')