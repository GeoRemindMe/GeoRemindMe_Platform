#coding=utf-8

from django.contrib.auth import authenticate, login
from django.core import serializers

from modules.jsonrpc import jsonrpc_method
from modules.jsonrpc.exceptions import InvalidCredentialsError, OtherError
from apps.profiles.forms import RegisterForm
from apps.events.models import Suggestion
from apps.places.models import Place
from modules.cities.models import City

from libs.mapsServices.places import GPRequest, GPAPIError


@jsonrpc_method('login(username=String, password=String) -> String', validate=True)
def api_login(request, username, password):
    user = authenticate(identification=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return request.session._session_key
        else:
            raise OtherError()
    raise InvalidCredentialsError()


@jsonrpc_method('register(username=String, email=String, password=String) -> String', validate=True)
def api_register(request, username, email, password):
    from userena import signals as userena_signals
    form = RegisterForm({'username': username,
                         'email': email,
                         'password1': password,
                         'password2': password
                     })
    if form.is_valid():
        new_user = form.save()
    else:
        raise InvalidCredentialsError("Data in use or invalid")
    
    userena_signals.signup_complete.send(sender=None,
                                         user=new_user)
    new_user.backend = 'django.contrib.auth.backends.ModelBackend' # HACK PARA LOGIN SIN CONOCER PASSWORD
    login(request, new_user)
    return request.session._session_key
    

@jsonrpc_method('places_near(lat=Number, lon=Number, accuracy=Number) -> Object', validate=True)
def api_places_near(request, lat, lon, accuracy=100):
    gp = GPRequest()
    places = gp.do_search(lat, lon, radius=accuracy)
    if places['status'] == 'OK':
    #places = Place.objects.nearest_to(lat=lat, lon=lon, accuracy=accuracy)
        i = iter(places['results'])
        places_to_return = {}
        for place in i:
            places_to_return.setdefault(place['id'], {
                                                      'name' : place['name'],
                                                      'address': place['vicinity'],
                                                      'location': {
                                                                   'lat': place['geometry']['location']['lat'],
                                                                   'lon': place['geometry']['location']['lng'],
                                                                   },
                                                      'types': place['types'],
                                                      'google_places_reference': place['reference'],
                                                      'icon': place['icon'],
                                                      })
        #p = Place.objects.filter(google_places_id__in=places_to_return.keys()).values_list('google_places_id', 'pk')
        return places_to_return if places_to_return else None
    return []


@jsonrpc_method('suggestions_near(lat=Number, lon=Number, accuracy=Number) -> Object', validate=False)
def api_suggestions_near(request, lat, lon, accuracy=100):
    suggestions = Suggestion.objects.nearest_to(lat=lat, lon=lon, accuracy=accuracy)
    json_serializer = serializers.get_serializer("json")()
    data = json_serializer.serialize(suggestions, ensure_ascii=False)
    return data

@jsonrpc_method('suggestion_detail(pk=Number) -> Object', validate=False)
def api_suggestion_detail(request, pk):
    suggestion = Suggestion.objects.filter(pk=pk, _vis='public')
    json_serializer = serializers.get_serializer("json")()
    data = json_serializer.serialize(suggestion, ensure_ascii=False)
    return data


@jsonrpc_method('city_current(lat=Number, lon=Number) -> Object', validate=True)
def api_city_current(request, lat, lon):
    city = City.objects.current(lat=lat, lon=lon)
    return city if city else None


@jsonrpc_method('backpack()', validate=True, authenticated=True)
def api_user_backpack(request):
    backpack = Suggestion.objects.get_backpack(follower=request.user)
    json_serializer = serializers.get_serializer("json")()
    data = json_serializer.serialize(backpack, ensure_ascii=False)
    return data
  