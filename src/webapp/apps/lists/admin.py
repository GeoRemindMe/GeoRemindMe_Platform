#coding=utf-8

from django.contrib import admin
from django.contrib.contenttypes import generic
from models import ListSuggestion, ListFollower, SuggestionInList


class ListFollowerInline(generic.GenericStackedInline):
    model = ListFollower
    extra = 1
    ct_field = "list_c_type"
    ct_fk_field = "list_id"
    readonly_fields  = ['created', 'modified']
    
    
class SuggestionInListInline(admin.StackedInline):
    model = SuggestionInList
    extra = 1


class ListSuggestionAdmin(admin.ModelAdmin):
    inlines = (ListFollowerInline, SuggestionInListInline)
    model = ListSuggestion
    fields = ['_vis', 'name', 'description', 'user', '_short_url', 'counter_followers']
    readonly_fields  = ['created', 'modified',]
    
    
admin.site.register(ListSuggestion, ListSuggestionAdmin)