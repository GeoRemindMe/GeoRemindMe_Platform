#coding=utf-8

from django.conf.urls.defaults import *
from respite.urls import resource, routes, templates

from views import *


urlpatterns = resource(
    prefix = '',
    views = SuggestionViews,
    routes = [
        # Route to backpack
        routes.route(
            regex = r'^(?P<username>[^/]+)/suggestions(?:\.[a-zA-Z]+)?/$',
            view = 'index',
            method = 'GET',
            name = 'events_suggestions_user'
        ),
        # Route to form for new suggestion
        routes.route(
            regex = r'^suggestion(?:\.[a-zA-Z]+)?/$',
            view = 'new',
            method = 'GET',
            name = 'events_suggestion_add'
        ),
        # Route to add a new suggestion
        routes.route(
            regex = r'^suggestion(?:\.[a-zA-Z]+)?/$',
            view = 'create',
            method = 'POST',
            name = 'events_suggestion_new'
        ),
        # Route to show a suggestion
        routes.route(
            regex = r'^suggestion/(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?/$',
            view = 'show',
            method = 'GET',
            name = 'events_suggestion_detail'
        ),
        routes.route(
            regex = r'^suggestion/(?P<slug>[^/.]+)(?:\.[a-zA-Z]+)?/$',
            view = 'show',
            method = 'GET',
            name = 'events_suggestion_detail'
        ),
        # Route to update a existing suggestion
        routes.route(
            regex = r'^suggestion/(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?/$',
            view = 'update',
            method = 'POST',
            name = 'events_suggestion_detail'
        ),
        routes.route(
            regex = r'^suggestion/(?P<slug>[^/.]+)(?:\.[a-zA-Z]+)?/$',
            view = 'update',
            method = 'POST',
            name = 'events_suggestion_detail'
        ),
        # Route to form to edit a existing suggestion
        routes.route(
            regex = r'^suggestion/(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?/edit/$',
            view = 'edit',
            method = 'GET',
            name = 'events_suggestion_edit'
        ),
        routes.route(
            regex = r'^suggestion/(?P<slug>[^/.]+)(?:\.[a-zA-Z]+)?/edit/$',
            view = 'edit',
            method = 'GET',
            name = 'events_suggestion_edit'
        ),
        # Route to get suggestions near
        routes.route(
            regex = r'^suggestions/near(?:\.[a-zA-Z]+)?/(?P<lat>[^/]+)/(?P<lon>[^/]+)/(?P<accuracy>[0-9]+)/$',
            view = 'near',
            method = 'GET',
            name = 'events_suggestions_near'
        ),
        # Route to form to edit a existing suggestion
        routes.route(
            regex = r'^suggestion/(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?/follow/$',
            view = 'follow',
            method = 'POST',
            name = 'events_suggestion_follow'
        ),
        # Route to form to edit a existing suggestion
        routes.route(
            regex = r'^suggestion/(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?/$',
            view = 'delete',
            method = 'DELETE',
            name = 'events_suggestion_delete'
        ),
    ]
)
