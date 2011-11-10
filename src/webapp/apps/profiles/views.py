# coding=utf-8

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from profiles.monkeys import *
from userena.views import profile_detail as userena_profile_detail
from userena.views import profile_edit as userena_profile_edit
from endless_pagination.decorators import page_template

from profiles.forms import UserProfileForm
from timelines.models import Timeline, Follower


@login_required
@page_template("profiles/dashboard_index_page.html")
def dashboard(request, extra_context=None):
    context = {
               'timelines' : Timeline.objects.get_chronology(user=request.user),
               }
    #Timeline.objects.add_timeline(request.user, 5, request.user, visible=True)    
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
                                edit_profile_form=form)

@page_template("profiles/profile_detail_index_page.html")
def profile_detail(request, username, extra_context=None):
    # TODO : (jneight) pintar timeline publico
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
