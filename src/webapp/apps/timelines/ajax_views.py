# coding=utf-8

from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.utils import simplejson

from libs.decorators import ajax_request
from models import Follower

@ajax_request
@login_required
def toggle_follower(request):
    """
    Añade un usuario como seguido por el usuario activo
        Parametros en POST
            userid : el id del usuario a seguir
            username : el username del usuario a seguir
        :returns: boolean
    """
    userid = request.POST.get('userid', None)
    if userid is not None:
        if userid == -1:
            return HttpResponseBadRequest()
        else:
            followee = get_object_or_404(User, pk = userid)
    else:
        username = request.POST.get('username', None)
        if username is not None:
            followee = get_object_or_404(User, username = username)
    if followee.id == -1:
        return HttpResponseBadRequest()
    
    added = Follower.objects.toggle_follower(follower = request.user,
                                             followee = followee)
    if added is None:
        return HttpResponseBadRequest()
    else:
        return HttpResponse(simplejson.dumps(added), mimetype="application/json")
    

@ajax_request
@login_required
def is_follower(request):
    """
    Comprueba si el usuario activo esta siguiendo a otro
        Parametros en POST
            userid : el id del usuario a seguir
            username : el username del usuario a seguir
        :returns: boolean
    """
    userid = request.POST.get('userid', None)
    if userid is not None:
        if userid == -1:
            return HttpResponseBadRequest()
        else:
            followee = get_object_or_404(User, pk = userid)
    else:
        username = request.POST.get('username', None)
        if username is not None:
            followee = get_object_or_404(User, username = username)
    if followee.id == -1:
        return HttpResponseBadRequest()
    
    is_follower = Follower.objects.is_follower(follower = request.user,
                                             followee = followee)
    
    return HttpResponse(simplejson.dumps(is_follower), mimetype="application/json")


@ajax_request
def get_followers(request):
    """
    Obtiene la lista de seguidores de un usuario.
    Si no se especifican parametros POST, se obtienen del usuario activo
        Parametros en POST
            userid : el id del usuario a seguir
            username : el username del usuario a seguir
        :returns: boolean
    """
    user = None
    userid = request.POST.get('userid', None)
    if userid is not None:
        if userid == -1:
            return HttpResponseBadRequest()
        else:
            user = User.objects.get(pk = userid)
    else:
        username = request.POST.get('username', None)
        if username is not None:
            user = User.objects.get(username__iexact = username)
    if user is None:
        if user.is_authenticated():
            user = request.user
        else:
            return HttpResponseBadRequest()
    elif user.id == -1:
        return HttpResponseBadRequest()
    
    followers = Follower.objects.get_by_follower(follower=user, type_filter=User)
    return HttpResponse(simplejson.dumps(followers), mimetype="application/json")

