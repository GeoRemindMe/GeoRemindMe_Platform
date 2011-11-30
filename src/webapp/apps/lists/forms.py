#coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from models import ListSuggestion


class ListSuggestionForm(forms.ModelForm):
    to_facebook = forms.BooleanField(label=_(u"Compartir en Facebook"), required=False
                                     )
    to_twitter = forms.BooleanField(label=_(u"Compartir en Twitter"), required=False
                                     )
    visibility = forms.CharField(required=False, initial='public')
    class Meta:
        model = ListSuggestion
        exclude = ('user', 'created', 'modified', '_short_url', '_vis')
    
    def save(self, user, ids=[]):
        if self.instance.id is not None and self.instance.user_id != user.id:
            raise PermissionDenied
        if self.instance.id is None: # sugerencia nueva
            listsuggestion = ListSuggestion.objects.create_from_ids(
                                 name = self.cleaned_data['name'],
                                 description = self.cleaned_data['description'],
                                 user = user, 
                                 suggestions = ids,
                                 _vis = self.cleaned_data.get('visibility', 'public'),
                                 to_facebook = self.cleaned_data['to_facebook'],
                                 to_twitter = self.cleaned_data['to_twitter'],
                     )
        else: # sugerencia ya existente
            self.instance.name = self.cleaned_data['name']
            self.instance.description = self.cleaned_data['description']
            self.instance.user = user
            self.instance._vis = self.cleaned_data.get('visibility', 'public'),
            self.instance.set_suggestions(ids=ids)
            self.instance.save()
            listsuggestion = self.instance
        return listsuggestion
