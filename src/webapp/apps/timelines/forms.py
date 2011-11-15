#coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _

from models import NotificationSettings

class NotificationSettingsForm(forms.Form):
    class Meta:
        model = NotificationSettings