#coding=utf-8

from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from profiles.monkeys import *
from userena.views import profile_detail as userena_profile_detail
from userena.views import profile_edit as userena_profile_edit
from userena.views import signup as userena_signup
from userena.views import signin as userena_signin
from endless_pagination.decorators import page_template
from socialregistration.contrib.facebook.models import FacebookProfile
from socialregistration.contrib.twitter.models import TwitterProfile

from profiles.forms import UserProfileForm
from timelines.models import Timeline, Follower
from models import UserProfile
from watchers import *


@login_required
@page_template("profiles/dashboard_index_page.html")
def dashboard(request, extra_context=None):
#    try:
#        request.user.get_profile()
#    except:
#        UserProfile.objects.create(user=request.user)
#    Timeline.objects.add_timeline(request.user, 0, request.user, visible=True)  
    context = {
               'timelines' : Timeline.objects.get_chronology(user=request.user),
               }
     
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response("profiles/dashboard.html",
                              context,
                              context_instance = RequestContext(request))

@login_required
def profile_edit(request, username):
    form = UserProfileForm
    return userena_profile_edit(request, 
                                username=username, 
                                template_name='profiles/profile_form.html',
                                edit_profile_form=form)

@page_template("profiles/profile_detail_index_page.html")
def profile_detail(request, username, extra_context=None):
    context = {
               'timelines' : Timeline.objects.get_by_user(user = username,
                                            visible = True)
               }
    if extra_context is not None:
        context.update(extra_context)
    return userena_profile_detail(request, 
                                  username=username, 
                                  template_name='profiles/profile_detail.html',
                                  extra_context = context)
    
def login(request):
    return userena_signin(request,
                          template_name='profiles/login.html')


def register(request):
    return userena_signup(request,
                          template_name = 'profiles/register.html',
                          success_url = '/dashboard/')
    
    
def user_avatar(request, username):
    profile = UserProfile.objects.filter(user__username=username)
    if profile is None:
        raise Http404
    return profile.get_mugshot_url()
