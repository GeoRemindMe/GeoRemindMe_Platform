# coding=utf-8

from respite.urls import resource, routes, templates

from views import *


urlpatterns = resource(
    prefix = 'suggestion/',
    views = SuggestionViews,
    routes = [
        # Route 'suggestions/' to the backpack view
        routes.route(
            regex = r'^(?:$|index(?:\.[a-zA-Z]+)/(?P<username>[^/]+)/$)',
            view = 'index',
            method = 'GET',
            name = 'events_suggestions_user'
        ),
        routes.route(
            regex = r'^create(?:\.[a-zA-Z]+)?/$',
            view = 'add',
            method = 'POST',
            name = 'api2_suggestion_create'
        ),
        routes.route(
            regex = r'^near(?:\.[a-zA-Z]+)?/(?P<lat>[^/]+)/(?P<lon>[^/]+)/(?P<accuracy>[0-9]+)/$',
            view = 'near',
            method = 'GET',
            name = 'api2_suggestion_update'
        ),
        routes.route(
            regex = r'^(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?/$',
            view = 'show',
            method = 'GET',
            name = 'api2_suggestion_detail'
        ),
        routes.route(
            regex = r'^(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?/$',
            view = 'update',
            method = 'POST',
            name = 'api2_suggestion_update'
        ),
    ]
)