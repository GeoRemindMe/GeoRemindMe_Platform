#coding=utf-8

from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views

from userena import views as userena_views
from userena import settings as userena_settings

import views as profiles_views

urlpatterns = patterns('',
    # Ver dashboard
    url(r'^dashboard/$',
       profiles_views.dashboard,
       name='profiles_dashboard'),
    # Editar perfil
    url(r'^!/(?P<username>[\.\w]+)/edit/$',
       profiles_views.profile_edit,
       name='profiles_profile_edit'),
    # Editar perfil
    url(r'^!/(?P<username>[\.\w]+)/picture/$',
       profiles_views.user_avatar,
       name='profiles_avatar'),
    # Ver perfil
    url(r'^!/(?P<username>[\.\w]+)/$',
       profiles_views.profile_detail,
       name='profiles_profile_public'),
    url(r'^users/(?P<page>[0-9]+)/$',
       userena_views.profile_list,
       name='profiles_profile_list_paginated'),
    url(r'^users/$',
       userena_views.profile_list,
       name='profiles_profile_list'),
    # Login, logout, registro
    url(r'^register/$',
       userena_views.signup,
       name='profiles_register'),
    url(r'^login/$',
       profiles_views.login,
       name='profiles_login'),
    url(r'^logout/$',
       auth_views.logout,
       {'next_page': userena_settings.USERENA_REDIRECT_ON_SIGNOUT,
        'template_name': 'profiles/logout.html'},
       name='profiles_logout'),
    # Reset password
    url(r'^password/reset/$',
       auth_views.password_reset,
       {'template_name': 'userena/password_reset_form.html',
        'email_template_name': 'userena/emails/password_reset_message.txt'},
       name='profiles_password_reset'),
    url(r'^password/reset/done/$',
       auth_views.password_reset_done,
       {'template_name': 'userena/password_reset_done.html'},
       name='profiles_password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm,
       {'template_name': 'userena/password_reset_confirm_form.html'},
       name='profiles_password_reset_confirm'),
    url(r'^password/reset/confirm/complete/$',
       auth_views.password_reset_complete,
       {'template_name': 'userena/password_reset_complete.html'}),
    # Change password
    url(r'^!/(?P<username>[\.\w]+)/password/$',
       userena_views.password_change,
       name='profiles_password_change'),
    url(r'^!/(?P<username>[\.\w]+)/password/complete/$',
       userena_views.direct_to_user_template,
       {'template_name': 'userena/password_complete.html'},
       name='profiles_password_change_complete'),
    # Change email and confirm it
    url(r'^!/(?P<username>[\.\w]+)/email/$',
       userena_views.email_change,
       name='profiles_email_change'),
    url(r'^!/(?P<username>[\.\w]+)/email/complete/$',
       userena_views.direct_to_user_template,
       {'template_name': 'userena/email_change_complete.html'},
       name='profiles_email_change_complete'),
    url(r'^!/(?P<username>[\.\w]+)/confirm-email/complete/$',
       userena_views.direct_to_user_template,
       {'template_name': 'userena/email_confirm_complete.html'},
       name='profiles_email_confirm_complete'),
    url(r'^!/(?P<username>[\.\w]+)/confirm-email/(?P<confirmation_key>\w+)/$',
       userena_views.email_confirm,
       name='profiles_email_confirm'),
   )
