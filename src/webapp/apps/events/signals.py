#coding=utf-8

import django.dispatch

suggestion_new = django.dispatch.Signal(providing_args=['to_facebook', 'to_twitter'])
suggestion_deleted = django.dispatch.Signal(providing_args=['user'])
suggestion_modified = django.dispatch.Signal(providing_args=['user'])
suggestion_following_new = django.dispatch.Signal(providing_args=['user'])
suggestion_following_deleted = django.dispatch.Signal(providing_args=['user'])
