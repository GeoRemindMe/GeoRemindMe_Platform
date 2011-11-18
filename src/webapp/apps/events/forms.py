#coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Suggestion
from widgets import *


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        exclude = ('user', 'created', 'modified', '_short_url')