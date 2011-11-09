# coding=utf-8

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from monkeys import *
from userena.views import profile_detail as userena_profile_detail
from userena.views import profile_edit as userena_profile_edit

from forms import UserProfileForm
from timelines.models import Timeline


@login_required
def dashboard(request):
    # TODO : (jneight) pintar timeline privado
    chrono = Timeline.objects.get_chronology(user=request.user)
    return render_to_response('profiles/dashboard.html',
                              {'timeline': chrono,},
                              context_instance = RequestContext(request))

@login_required
def profile_edit(request, username):    
    form = UserProfileForm
    return userena_profile_edit(request, 
                                username=username, 
                                edit_profile_form=form)

def profile_detail(request, username):
    # TODO : (jneight) pintar timeline publico
    timeline = Timeline.objects.get_by_user(user = request.user,
                                            visible = True)
    return userena_profile_detail(request, username=username, extra_context = {'timeline': timeline})
