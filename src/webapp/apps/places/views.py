#coding=utf-8

from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from endless_pagination.decorators import page_template

from models import Place, City, Region, Country
from forms import PlaceForm


@login_required
def place_edit(request, slug):
    place = get_object_or_404(Place, slug__iexact=slug)
    if request.method == 'POST':
        form = PlaceForm(request.POST, instance=place)
        if form.is_valid():
            form.save()
            return HttpResponse(place.get_absolute_url())
    else:
        form = PlaceForm(instance=place)
    return render_to_response('places/place_edit.html',
                              {'form': form},
                              context_instance = RequestContext(request))
    

def place_detail(request, slug):
    try:
        place = Place.objects.select_related('city__region__country').get(slug__iexact=slug)
    except Place.DoesNotExist:
        raise Http404
    suggestions = place.suggestion_set.select_related('user')
    return render_to_response('places/place_detail.html',
                              {'place': place,
                               'suggestions_q': suggestions,
                              }, 
                              context_instance = RequestContext(request))


@login_required
def place_add(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            new_place = form.save()
            return HttpResponse(new_place.get_absolute_url())
    else:
        form = PlaceForm()
    return render_to_response('places/place_edit.html',
                              {'form': form,
                               'new': True 
                              },
                              context_instance = RequestContext(request))


@page_template("places/places_list_index_page.html")
def places_list(request, extra_context=None):
    context = {
               'places' : Place.objects.all().select_related()
               }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response('places/places_list.html',
                              context,
                              extra_context = RequestContext(request))
