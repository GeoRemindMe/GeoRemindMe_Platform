#coding=utf-8

import django.dispatch

list_new = django.dispatch.Signal(providing_args=['to_facebook', 'to_twitter'])
list_deleted = django.dispatch.Signal(providing_args=['user'])
list_modified = django.dispatch.Signal(providing_args=['user'])
list_following_added = django.dispatch.Signal(providing_args=['follower'])
list_following_deleted = django.dispatch.Signal(providing_args=['follower'])