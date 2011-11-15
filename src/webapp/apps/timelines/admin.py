#coding=utf-8

from django.contrib import admin
from models import Timeline, TimelineFollower, Follower


admin.site.register(Follower)
admin.site.register(Timeline)
admin.site.register(TimelineFollower)