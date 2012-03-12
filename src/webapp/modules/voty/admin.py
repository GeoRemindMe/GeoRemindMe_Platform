# coding=utf-8

from django.contrib import admin

from reversion.admin import VersionAdmin
from models import Vote

admin.site.register(Vote, VersionAdmin)