#coding=utf-8

from django.contrib import admin
from django.contrib.contenttypes import generic
from models import Timeline, TimelineFollower, Follower, TimelineNotification


class TimelineFollowerInline(generic.GenericStackedInline):
    model = TimelineFollower
    extra = 1
    ct_field = "follower_c_type"
    ct_fk_field = "follower_id"
    

class TimelineAdmin(admin.ModelAdmin):
    inlines = (TimelineFollowerInline,)
    model = Timeline



admin.site.register(Follower)
admin.site.register(Timeline, TimelineAdmin)
admin.site.register(TimelineNotification)