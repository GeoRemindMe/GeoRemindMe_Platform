#coding=utf-8

import django.dispatch

list_new = django.dispatch.Signal(providing_args=['to_facebook', 'to_twitter'])
