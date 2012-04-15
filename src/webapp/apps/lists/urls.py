#coding=utf-8

from django.conf.urls.defaults import *
from respite.urls import resource, routes, templates

from views import *

urlpatterns = resource(
    prefix = '',
    views = ListSuggestionViews,
    routes = [
            # Route to form for new suggestion
            routes.route(
                 regex = r'^ls(?:\.[a-zA-Z]+)?/$',
                 view = 'new',
                 method = 'GET',
                 name = 'lists_suggestion_add'
            ),
            # Route to list
            routes.route(
                regex = r'^ls/(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?/$',
                view = 'show',
                method = 'GET',
                name = 'events_suggestion_detail'
            ),
            # Route to form to edit a existing list
            routes.route(
                regex = r'^ls/(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?/edit/$',
                view = 'edit',
                method = 'GET',
                name = 'lists_suggestion_edit'
            ),
            # Route to update a existing list
            routes.route(
                regex = r'^ls/(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?/$',
                view = 'update',
                method = 'POST',
                name = 'lists_suggestion_detail'
            ),
  ]
)
