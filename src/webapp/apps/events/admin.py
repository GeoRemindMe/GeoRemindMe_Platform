#coding=utf-8

from django.contrib import admin
from django.contrib.contenttypes import generic
from models import Suggestion, EventFollower


class EventFollowerInline(generic.GenericStackedInline):
    model = EventFollower
    extra = 1
    ct_field = "event_c_type"
    ct_fk_field = "event_id"

class SuggestionAdmin(admin.ModelAdmin):
    inlines = (EventFollowerInline,)
    model = Suggestion
    fields = ['_vis', 'name', 'description', 'user', 'place', 'done', 'date_starts', 'date_ends', '_short_url', 'counter_followers', 'location']
    readonly_fields  = ['created', 'modified', 'slug', 'location']
    
    
admin.site.register(Suggestion, SuggestionAdmin)