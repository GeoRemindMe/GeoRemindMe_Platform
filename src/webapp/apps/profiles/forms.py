#coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _

from userena.forms import USERNAME_RE

from models import UserProfile


class UserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        
        
class UserProfileForm(forms.ModelForm):
    
    username = forms.RegexField(regex=USERNAME_RE,
                                max_length=15,
                                min_length=4,
                                widget=forms.TextInput(attrs={'class': 'required'}),
                                label=_(u"Nombre de usuario"),
                                error_messages={'invalid': _(u"El nombre de usuario solo "\
                                                             "debe tener letras, numeros, "\
                                                             "numeros, puntos o guiones bajos")})
    class Meta:
        model = UserProfile
        fields = ( 'show_followers', 'show_followings', 
                  'language', 'privacy', 'sync_avatar_with', 'privacy',
                  'description')
        exclude = ('user', 'slug', 'mugshot',)
        
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        new_order = self.fields.keyOrder[:-1]
        new_order.insert(0, 'username')
        self.fields.keyOrder = new_order
        
    def save(self, force_insert=False, force_update=False, commit=True):
        profile = super(self.__class__, self).save(commit=commit)
        #guardar nombre de usuario
        user = profile.user
        user.username = self.cleaned_data['username']
        user.save()

        