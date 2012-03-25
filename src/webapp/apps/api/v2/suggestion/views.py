# coding=utf-8


from django.http import HttpResponse, HttpResponseBadRequest
from django.http import Http404
from django.contrib.auth.models import User

from respite import Views
from respite.decorators import override_supported_formats

from apps.events.models import Suggestion
from apps.events.forms import SuggestionForm
from apps.lists.models import ListSuggestion




class SuggestionViews(Views):
    supported_formats = ['json', 'xml']
    
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
               pass
            follower = user
        else:
            follower = request.user
        suggestions = Suggestion.objects.get_backpack(follower=follower)
        lists = ListSuggestion.objects.get_by_follower(follower=follower)
        
        
        return self._render(
                            request = request,
                            template = 'events/suggestions_user',
                            context = {
                                       'suggestion': suggestions,
                                       },
                            status = 200)
    
    def show(self, request, id):
        """
            SHOW A SUGGESTION FROM ITS ID
        """
        try:
             suggestion = Suggestion.objects.has_voted(request.user
                                                         ).select_related('user', 
                                                                         'place__city__region__country',
                                                                         ).get(pk=id)
        except Suggestion.DoesNotExist:
            return self._render(
                         request = request,
                         status = 404
                         )
        if not suggestion._is_public() and suggestion.user_id != request.user.id:
            return self._forbidden(request)
        return self._render(
                             request = request,
                             context = {'suggestion': suggestion },
                             status = 200
                             )
       
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

    def create(self, request):
        """
            CREATES A NEW SUGGESTION
        """
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = self._create_or_update(request, form)
            return self._render(
                        request = request,
                        context = {
                                   'suggestion': suggestion,
                                   },
                        status = 200)
        return self._badrequest(request, {'msg': 'invalid id'})
        
    def update(self, request, id):
        """
            UPDATE A EXISTING SUGGESTION
        """
        try:
            suggestion = Suggestion.objects.get(pk=id, user=request.user)
        except Suggestion.DoesNotExist:
            return self._notfound(request)
        form = SuggestionForm(request.POST, instance=suggestion)
        if form.is_valid():
            suggestion = self._create_or_update(request, form)
            return self._render(
                                request = request,
                                context = {
                                           'suggestion': suggestion,
                                           },
                                status = 200)
        return self._badrequest(request, {'msg': 'invalid id'})
        
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
