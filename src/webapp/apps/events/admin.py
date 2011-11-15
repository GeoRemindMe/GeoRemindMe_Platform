#coding=utf-8

from django.contrib import admin
from models import Suggestion, EventFollower


admin.site.register(EventFollower)
admin.site.register(Suggestion)