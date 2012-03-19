#coding=utf-8

"""
.. module:: webapp.apps.api.views
    :platform: GeoRemindMe!
    :synopsis: API functions
"""


from django.contrib.auth import authenticate, login
from django.core import serializers

from modules.jsonrpc import jsonrpc_method
from modules.jsonrpc.exceptions import InvalidCredentialsError, OtherError
from apps.profiles.forms import RegisterForm
from apps.events.models import Suggestion
from apps.events.forms import SuggestionForm
from apps.places.models import Place
from modules.cities.models import City

from libs.mapsServices.places import GPRequest, GPAPIError


@jsonrpc_method('login(username=String, password=String) -> String', validate=True)
def api_login(request, username, password):
    """
        Logs a user in the system
        
        :param username: Username or email
        :type username: string
        :param password: User's password
        :type password: string
        
        :return: session id
        :raises: InvalidCredentialsError or OtherError
    """
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
    """
        Register a new user in the system
        
        :param username: Usernamel
        :type username: string
        :param email: Email
        :type email: string
        :param password: User's password
        :type password: string
        
        :return: session id if registration success
        :raises: InvalidCredentialsError or OtherError
    """
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
    """
        Returns the places near to the location
        
        :param lat: Latitude
        :type username: float
        :param lon: Longitude 
        :type password: float
        :param accuracy: max distance requested (in meters)
        :type accuracy: integer
        
        
        :return:
            >>> places_near(37,-3,500)
                Requesting ->
                    {"id":"jsonrpc", "params":[37, -3, 500], "method":"places_near", "jsonrpc":"1.0"}
                Got ->
                    {"error": null, "jsonrpc": "1.0", "id": "jsonrpc", "result": {"c644dcd3f743006f34c687255fae5eb02f5de004": {"google_places_reference": "CnRmAAAAzEJrzob6u9wO3cZhZH7frAEDQxNtUWFgSrINsuBsM6Pc8ECe4zm0yjfywFNuG2yH5cbYFIQikOlmFPGA0YKN9RrPMghlmLTDNl_wpHqs6-AR_aRLPmyj-DanAuOUJ8F9_y61Rvhj8CFHMOCX6RnuCRIQxKtyARYpHWK784L_vV_Z6hoUudfADvedbL-zgjEFbVmXSnDTDz0", "name": "Nevada", "location": {"lat": 37.0, "lon": -3.0166667}, "address": "Nevada", "types": ["locality", "political"], "icon": "http://maps.gstatic.com/mapfiles/place_api/icons/geocode-71.png"}}}        
    """
    gp = GPRequest()
    places = gp.do_search(lat, lon, radius=accuracy)
    if places['status'] == 'OK':
    #places = Place.objects.nearest_to(lat=lat, lon=lon, accuracy=accuracy)
        i = iter(places['results'])
        places_to_return = {}
        for place in i:
            places_to_return.setdefault(place['id'], {
                                                      'name' : place['name'],
                                                      'address': place.get('vicinity'),
                                                      'location': {
                                                                   'lat': place['geometry']['location']['lat'],
                                                                   'lon': place['geometry']['location']['lng'],
                                                                   },
                                                      'types': place['types'],
                                                      'google_places_reference': place['reference'],
                                                      'icon': place['icon'],
                                                      })
        #p = Place.objects.filter(google_places_id__in=places_to_return.keys()).values_list('google_places_id', 'pk')
        return places_to_return if places_to_return else {}
    return {}


@jsonrpc_method('suggestions_near(lat=Number, lon=Number, accuracy=Number) -> Object', validate=False)
def api_suggestions_near(request, lat, lon, accuracy=100):
    """
        Returns the suggestions near to the location
        
        :param lat: Latitude
        :type username: float
        :param lon: Longitude 
        :type lon: float
        :param accuracy: max distance requested (in meters)
        :type accuracy: integer
        
        
        :return: 
            >>> suggestions_near(37,-3,500000)
                Requesting ->
                    {"id":"jsonrpc", "params":[37, -3, 500000], "method":"suggestions_near", "jsonrpc":"1.0"}
                Got ->
                    {"error": null, "jsonrpc": "1.0", "id": "jsonrpc", "result": "[{\"pk\": 4, \"model\": \"events.suggestion\", \"fields\": {\"user\": [1, \"admin\"], \"place\": [4, \"GeoRemindMe!\", \"Avenida de la Innovaci\u00f3n 1, CADE, M\u00f3dulo 11, 18100 Armilla, Granada, Espa\u00f1a\", \"Armilla\", [37.147712, -3.609319], \"92e1cc75513c4dcac6a6d0f72b2632150d4d3115\"], \"name\": \"visita georemindme\", \"description\": \"\"}}]"}
    """
    suggestions = Suggestion.objects.nearest_to(lat=lat, lon=lon, accuracy=accuracy)
    return Suggestion.serialize_to_json(suggestions)


@jsonrpc_method('suggestion_detail(pk=Number) -> Object', validate=False)
def api_suggestion_detail(request, pk):
    """
        Returns a suggestion
        ignored
        :param lat: Latitude
        :type username: float
        :param lon: Longitude 
        :type lon: float
        
        :return: Suggestion
    """
    suggestion = Suggestion.objects.filter(pk=pk, _vis='public')
    return Suggestion.serialize_to_json(suggestion)


@jsonrpc_method('suggestion_add(name=String, description=String, place=Object) -> Object', validate=False, authenticated=True)
def api_suggestion_add(request, name, description, place):
    place_obj = None
    if type(place) == type(0):
        place_obj = Place.objects.filter(pk=place)
    if place_obj is None:
        place_obj = Place.objects.create_from_google(
                                 google_places_reference = place,
                                 user = request.user
                                 )
        
    data = {
            'name': name,
            'description': description,
            'visibility': 'public',
            }
    form = SuggestionForm(data)
    if form.is_valid():
        suggestion = form.save(user=request.user, place=place_obj)
        return Suggestion.serialize_to_json([suggestion])
    return form.errors


@jsonrpc_method('city_current(lat=Number, lon=Number) -> Object', validate=True)
def api_city_current(request, lat, lon):
    """
        Returns the current city
        
        :param lat: Latitude
        :type lat: float
        :param lon: Longitude 
        :type lon: float
        
        :return:
            >>> city_current(37,-3)
                Requesting ->
                    {"id":"jsonrpc", "params":[37, -3], "method":"city_current", "jsonrpc":"1.0"}
                Got ->
                    {"error": null, "jsonrpc": "1.0", "id": "jsonrpc", "result": "[{\"pk\": 2513124, \"model\": \"cities.city\", \"fields\": {\"_order\": 0, \"name\": \"Olocau\", \"region\": 57, \"location\": \"POINT (39.7000000000000028 -0.5333300000000000)\", \"slug\": \"olocau_valencia_spain\", \"population\": 1127}}]"}
    """
    city = City.objects.current(lat=lat, lon=lon)
    json_serializer = serializers.get_serializer("json")()
    data = json_serializer.serialize(city, ensure_ascii=False)
    return data


@jsonrpc_method('backpack()', validate=True, authenticated=True)
def api_user_backpack(request):
    """
        Return the user's backpack. Requires authentication
        
        :return: Suggestions
    """
    backpack = Suggestion.objects.get_backpack(follower=request.user)
    return Suggestion.serialize_to_json(backpack)
