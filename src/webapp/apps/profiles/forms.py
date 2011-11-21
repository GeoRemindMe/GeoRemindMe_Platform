#coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from userena.forms import USERNAME_RE, identification_field_factory
from userena import settings as userena_settings

from models import UserProfile

attrs_dict = {'class': 'required'}

class UserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        
        
class UserProfileForm(forms.ModelForm):
    username = forms.RegexField(regex=USERNAME_RE,
                                max_length=15,
                                min_length=4,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_(u"Nombre de usuario"),
                                error_messages={'invalid': _(u"El nombre de usuario solo "\
                                                             "debe tener letras, numeros, "\
                                                             "numeros, puntos o guiones bajos")})
    class Meta:
        model = UserProfile
        fields = ( 'show_followers', 'show_followings', 
                  'language', 'privacy', 'sync_avatar_with', 'privacy',
                  'description', 'favorite_location')
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
        
        
class LoginForm(forms.Form):
    """
    A custom form where the identification can be a e-mail address or username.

    """
    email = identification_field_factory(_(u"Email o nombre de usuario"),
                                                  _(u"Indica tu email o nombre de usuario."))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                                     required=False,
                                     label=_(u'Recordarme por %(days)s') % {'days': _(userena_settings.USERENA_REMEMBER_ME_DAYS[0])})
    _user = None

    def clean(self):
        """
        Checks for the identification and password.

        If the combination can't be found will raise an invalid sign in error.

        """
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(identification=email, password=password)
            if user is None:
                raise forms.ValidationError(_(u"Por favor, introduce un nombre de usuario, email o contraseña correcta."))
            self._user = user
        return self.cleaned_data
    

class RegisterForm(forms.Form):
    """
    Form for creating a new user account.

    Validates that the requested username and e-mail is not already in use.
    Also requires the password to be entered twice and the Terms of Service to
    be accepted.

    """
    username = forms.RegexField(regex=USERNAME_RE,
                                max_length=15,
                                min_length=4,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _('El nombre solo debe tener letras, numeros, puntos y guiones bajos.')})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("Email"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Contraseña"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Repetir contraseña"))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already in use.
        Also validates that the username is not listed in
        ``USERENA_FORBIDDEN_USERNAMES`` list.

        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(_('Nombre de usuario ya existente.'))
        if self.cleaned_data['username'].lower() in userena_settings.USERENA_FORBIDDEN_USERNAMES:
            raise forms.ValidationError(_('Nombre de usuario invalido.'))
        return self.cleaned_data['username']

    def clean_email(self):
        """ Validate that the e-mail address is unique. """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_('Email ya en uso, por favor, registrate con otro diferente.'))
        return self.cleaned_data['email']

    def clean(self):
        """
        Validates that the values entered into the two password fields match.
        Note that an error here will end up in ``non_field_errors()`` because
        it doesn't apply to a single field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_('Las contraseñas deben ser iguales.'))
        return self.cleaned_data

    def save(self):
        """ Creates a new user and account. Returns the newly created user. """
        username, email, password = (self.cleaned_data['username'],
                                     self.cleaned_data['email'],
                                     self.cleaned_data['password1'])
        from userena.models import UserenaSignup
        new_user = UserenaSignup.objects.create_user(username,
                                                     email, 
                                                     password,
                                                     not userena_settings.USERENA_ACTIVATION_REQUIRED,
                                                     userena_settings.USERENA_ACTIVATION_REQUIRED)
        return new_user

        