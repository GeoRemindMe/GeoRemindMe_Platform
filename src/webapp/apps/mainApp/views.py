#coding=utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

def home(request, logged=False):
    if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('profiles_dashboard'))
    return render_to_response("mainApp/home.html", 
                              {'logged' : logged}, 
                              context_instance=RequestContext(request)
                              )
    