#coding=utf-8

from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from respite import Views
from respite.decorators import override_supported_formats, login_required

from apps.events.models import Suggestion
from apps.events.forms import SuggestionForm
from apps.lists.models import ListSuggestion


class SuggestionViews(Views):
    supported_formats = ['html', 'json', 'xml']
    
    @login_required
    def index(self, request, username):
        """
            RETURN THE BACKPACK
        """
        if username and username != request.user.username:
            try:
                user = User.objects.select_related('profile').get(
                                                      username=username.lower()
                                                      )
            except User.DoesNotExist:
                return self._notfound(request)
            if not user.profile.can_view_profile(request.user):
                return self._forbidden(request)
            follower = user
        else:
            follower = request.user
        suggestions = Suggestion.objects.get_backpack(follower=follower)
        lists = ListSuggestion.objects.get_by_follower(follower=follower)
        
        return self._render(
                            request = request,
                            template = 'events/suggestions_user',
                            context = {
                                       'suggestions_q': suggestions,
                                       'lists_q': lists,
                                       },
                            status = 200)
    
    
    def show(self, request, id=None, slug=None):
        """
            SHOW A SUGGESTION FROM ITS ID
        """
        try:
            suggestion = Suggestion.objects.has_voted(request.user
                                                         ).select_related('user', 
                                                                         'place__city__region__country',
                                                                         )
            if id:
                suggestion = suggestion.get(pk=id)
            else:
                suggestion = suggestion.get(slug=slug.lower())
        except Suggestion.DoesNotExist:
            return self._notfound(request)
        if not suggestion._is_public() and suggestion.user_id != request.user.id:
            return self._forbidden(request)
        return self._render(
                             request = request,
                             template = 'events/suggestion_detail',
                             context = {'suggestion': suggestion },
                             status = 200
                             )

    @login_required
    def new(self, request):
        """
            RETURNS THE FORM TO CREATE A NEW SUGGESTION
        """
        form = SuggestionForm()
        return self._render(
                        request = request,
                        template = 'events/suggestion_new',
                        context = {
                                   'form': form,
                                   },
                        status = 200)
    
    @login_required
    def create(self, request):
        """
            CREATES A NEW SUGGESTION
        """
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = self._create_or_update(request, form)
            return self._render(
                        request = request,
                        template = 'events/suggestion_detail',
                        context = {
                                   'suggestion': suggestion,
                                   },
                        status = 200)
        return self._badrequest(request, {'msg': 'invalid id'})
        
    @login_required
    def update(self, request, id=None, slug=None):
        """
            UPDATE A EXISTING SUGGESTION
        """
        try:
            if id:
                suggestion = Suggestion.objects.get(pk=id, user=request.user)
            else:
                suggestion = Suggestion.objects.get(slug=slug.lower(), user=request.user)
        except Suggestion.DoesNotExist:
            return self._notfound(request)
        form = SuggestionForm(request.POST, instance=suggestion)
        if form.is_valid():
            suggestion = self._create_or_update(request, form)
            return self._render(
                                request = request,
                                template = 'events/suggestion_detail',
                                context = {
                                           'suggestion': suggestion,
                                           },
                                status = 200)
        return self._badrequest(request, {'msg': 'invalid id'})
    
    @login_required
    def edit(self, request, id=None, slug=None):
        """
            RETURNS THE FORM TO EDIT A EXISTING SUGGESTION
        """
        try:
            if id:
                suggestion = Suggestion.objects.get(pk=id, user=request.user)
            else:
                suggestion = Suggestion.objects.get(slug=slug.lower(), user=request.user)
        except Suggestion.DoesNotExist:
            return self._notfound(request)
        form = SuggestionForm(instance=suggestion)
        return self._render(
                                request = request,
                                template = 'events/suggestion_new',
                                context = {
                                           'form': form,
                                           },
                                status = 200)
    
    @override_supported_formats(['json', 'xml'])
    def near(self, request, lat, lon, accuracy = 500):
        """
            RETURNS A LIST OF SUGGESTION NEAR THE LAT,LON
        """
        suggestions = Suggestion.objects.nearest_to(lat=lat, lon=lon, accuracy=accuracy)
        return self._render(
                            request = request,
                            context = {'suggestions': suggestions},
                            status = 200
                            )

    @login_required
    @override_supported_formats(['json', 'xml'])
    def delete(self, request, id):
        try:
            suggestion = Suggestion.objects.get(pk=id, user=request.user)
        except Suggestion.DoesNotExist:
            return self._notfound(request)
        deleted = suggestion.delete()
        return self._render(
                            request = request,
                            context = {'suggestions': suggestions},
                            status = 200
                            )
        
    @override_supported_formats(['json', 'xml'])
    @login_required
    def follow(self, request, id):
        try:
            suggestion = Suggestion.objects.get(pk=id)
        except Suggestion.DoesNotExist:
            return self._notfound(request)
        follower = Suggestion.objects.toggle_follower(follower = request.user,
                                             suggestion=suggestion)
        return self._render(
                        request = request,
                        context = { 'follower': follower},
                        status = 200
                        )
    
        
    def _create_or_update(self, request, form):
        poi_id = request.POST.get('poi_id', '')
        place = None
        if poi_id != '':
            place = get_object_or_404(Place, pk=poi_id)
        else:
            place_reference = request.POST.get('place_reference', '')
            if place_reference != '':
                place = Place.objects.create_from_google(
                                     google_places_reference = place_reference,
                                     user = request.user
                                     )
        return form.save(user=request.user, place=place)
    
