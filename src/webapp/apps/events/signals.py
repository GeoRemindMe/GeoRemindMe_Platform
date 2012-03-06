#coding=utf-8

import django.dispatch

suggestion_new = django.dispatch.Signal(providing_args=['to_facebook', 'to_twitter'])

