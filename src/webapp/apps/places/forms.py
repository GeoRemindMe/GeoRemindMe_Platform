#coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Place


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        exclude = ('user', 'google_places_reference', 'google_places_id')