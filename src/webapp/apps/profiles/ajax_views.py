#coding=utf-8

from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from userena.decorators import secure_required

from libs.decorators import ajax_request


@ajax_request
@secure_required
@never_cache
def login(request):
    from forms import LoginForm
    from userena import settings as userena_settings
    form = LoginForm(request.POST)
    if form.is_valid():
            if form._user.is_active:
                from django.contrib.auth import login
                login(request, form._user)
                if form.cleaned_data['remember_me']:
                    request.session.set_expiry(userena_settings.USERENA_REMEMBER_ME_DAYS[1] * 86400)
                else: request.session.set_expiry(0)
                if userena_settings.USERENA_USE_MESSAGES:
                    from django.contrib import messages
                    messages.success(request, _('Bienvenido %s' % form._user.username),
                                     fail_silently=True)

                # Whereto now?
                from userena.utils import signin_redirect
                redirect_to = signin_redirect(
                    request.REQUEST.get('next'), form._user)
                return redirect(redirect_to)
            else:
                return redirect(reverse('profiles_disabled',
                                        kwargs={'username': form._user.username}))
                
@ajax_request
@secure_required
@never_cache
def register(request):
    from forms import RegisterForm
    form = RegisterForm(request.POST)
    if form.is_valid():
        from django.contrib.auth import login, logout
        from userena import settings as userena_settings
        user = form.save()
        # Send the signup complete signal
        from userena import signals as userena_signals
        userena_signals.signup_complete.send(sender=None,
                                             user=user)
        if request.POST.get('success_url'): redirect_to = request.POST['success_url']
        else: redirect_to = reverse('userena_signup_complete',)
        # A new signed user should logout the old one.
        if request.user.is_authenticated():
            logout(request)
        login(request, user)
        if userena_settings.USERENA_USE_MESSAGES:
            from django.contrib import messages
            messages.success(request, _('Bienvenido %s' % user.username),
                             fail_silently=True)
        return redirect(redirect_to)