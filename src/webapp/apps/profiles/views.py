#coding=utf-8

from django.http import HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import F

from profiles.monkeys import *
from userena.views import profile_edit as userena_profile_edit
from userena.views import signup as userena_signup
from endless_pagination.decorators import page_template


from profiles.forms import UserProfileForm
from timelines.models import Timeline, Follower, TimelineNotification
from models import UserProfile


@login_required
@page_template("generic/timeline.html")
def dashboard(request, extra_context=None):
    context = {
               'objects' : request.user.get_chronology(),
               }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response("profiles/dashboard.html",
                              context,
                              context_instance = RequestContext(request))


@login_required
@page_template("profiles/notifications_index_page.html")
def notifications(request, extra_context=None):
    context = {
               'objects': request.user.get_notifications()
               }
    UserProfile.objects.set_notifications(request.user, value=-10)
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response("profiles/notifications.html",
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
    try:
        user = User.objects.select_related('profile').get(
                                                      username=username
                                                      )
    except User.DoesNotExist:
        raise Http404
    if not user.profile.can_view_profile(request.user):
        return HttpResponseForbidden(_("No tienes permiso para ver este perfil"))
    
    context = {
               'profile': user.profile,
               'objects' : Timeline.objects.get_by_user(user = username,
                                            visible = True),
               'user_profile': user,
               'is_follower': Follower.objects.is_follower(request.user, user),
               'is_following': Follower.objects.is_follower(user, request.user),
               }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response('profiles/profile_detail.html',
                              context,
                              context_instance = RequestContext(request))

    
def register(request):
    return userena_signup(request,
                          template_name = 'profiles/register.html',
                          success_url = '/dashboard/')
    
    
def user_avatar(request, username):
    try:
        user = User.objects.select_related('profile').get(
                                                      username__iexact=username
                                                      )
    except User.DoesNotExist:
        raise Http404
    return user.profile.get_mugshot_url()


@page_template("profiles/profile_followers_index_page.html")
def followers_panel(request, username, extra_context=None):
    try:
        user = User.objects.select_related('profile').get(
                                                      username__iexact=username
                                                      )
    except User.DoesNotExist:
        raise Http404
    if not user.profile.can_view_profile(request.user) or not user.profile.show_followers:
        return HttpResponseForbidden(_("No tienes permiso para ver este perfil"))
    
    followers = user.followees.all() # who has the user as followee, so they are followers :=
    context = {
               'objects': followers,
               'username': username
               }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response('profiles/profile_followers.html',
                              context,
                              context_instance=RequestContext(request)
                              )


@page_template("profiles/profile_followers_index_page.html")
def followings_panel(request, username, extra_context=None):
    try:
        user = User.objects.select_related('profile').get(
                                                      username__iexact=username
                                                      )
    except User.DoesNotExist:
        raise Http404
    if not user.profile.can_view_profile(request.user) or not user.profile.show_followings:
        return HttpResponseForbidden(_("No tienes permiso para ver este perfil"))
    
    followees = user.followers.all()
    context = {
               'objects': followees,
               'username': username
               }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response('profiles/profile_followings.html',
                              context,
                              context_instance=RequestContext(request)
                              )
