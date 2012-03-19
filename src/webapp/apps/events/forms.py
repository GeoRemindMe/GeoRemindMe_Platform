#coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from models import Suggestion


class SuggestionForm(forms.ModelForm):
    to_facebook = forms.BooleanField(label=_(u"Compartir en Facebook"), required=False
                                     )
    to_twitter = forms.BooleanField(label=_(u"Compartir en Twitter"), required=False
                                     )
    visibility = forms.CharField(required=False, initial='public')
    
    class Meta:
        model = Suggestion
        exclude = ('user', 'created', 'modified', '_short_url', 'place', '_vis')
        
    def clean(self):
        if self.cleaned_data['date_starts'] is not None and self.cleaned_data['date_ends']:
            if self.cleaned_data['date_starts'] >= self.cleaned_data['date_ends']:            
                msg = _("Fechas incorrectas")
                self._errors['starts'] = self.error_class([msg])
        return self.cleaned_data
    
    def save(self, user, place = None):
        if self.instance.id is None and place is None:
            raise KeyError("place needed")
        if self.instance.id is not None and self.instance.user_id != user.id:
            raise PermissionDenied()
        if self.instance.id is None: # sugerencia nueva
            suggestion = Suggestion.objects.create(
                                 name = self.cleaned_data['name'],
                                 description = self.cleaned_data['description'],
                                 date_starts = self.cleaned_data['date_starts'],
                                 date_ends = self.cleaned_data['date_ends'],
                                 place = place,
                                 user = user, 
                                 done = self.cleaned_data.get('done', False),
                                 _vis = self.cleaned_data.get('visibility', 'public'),
                                 to_facebook = self.cleaned_data['to_facebook'],
                                 to_twitter = self.cleaned_data['to_twitter'],
                     )
        else: # sugerencia ya existente
            self.instance.name = self.cleaned_data['name']
            self.instance.description = self.cleaned_data['description']
            self.instance.date_starts = self.cleaned_data['date_starts']
            self.instance.date_ends = self.cleaned_data['date_ends']
            self.instance.place = place
            self.instance.user = user
            self.instance.done = self.cleaned_data.get('done', False)
            self.instance._vis = self.cleaned_data.get('visibility', 'public'),
            self.instance.save()
            suggestion = self.instance
        return suggestion

