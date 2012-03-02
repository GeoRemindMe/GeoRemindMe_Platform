#coding=utf-8

import django.dispatch


place_new = django.dispatch.Signal(providing_args=['user'])
place_deleted = django.dispatch.Signal(providing_args=['user'])
place_modified = django.dispatch.Signal(providing_args=['user'])