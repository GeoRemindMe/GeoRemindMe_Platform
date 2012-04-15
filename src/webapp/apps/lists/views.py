#coding=utf-8

from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from respite import Views
from respite.decorators import override_supported_formats, login_required

from apps.lists.forms import ListSuggestionForm
from apps.lists.models import ListSuggestion


class ListSuggestionViews(Views):
    supported_formats = ['html', 'json', 'xml']
    
    def show(self, request, id):
        """
            SHOW A LISTSUGGESTION FROM ITS ID
        """
        try:
            ls = ListSuggestion.objects.has_voted(request.user
                                                         ).select_related('user', 
                                                                         'place__city__region__country',
                                                                         ).get(pk=id)
        except ListSuggestion.DoesNotExist:
            return self._notfound(request)
        if not ls.is_public() and ls.user_id != request.user.id:
            return self._forbidden(request)
        return self._render(
                             request = request,
                             template = 'lists/listsuggestion_detail',
                             context = {'list': ls },
                             status = 200
                             )

    @login_required
    def new(self, request):
        """
            RETURNS THE FORM TO CREATE A NEW LISTSUGGESTION
        """
        form = ListSuggestionForm()
        return self._render(
                        request = request,
                        template = 'lists/listsuggestion_new',
                        context = {
                                   'form': form,
                                   },
                        status = 200)
    
    @login_required
    def create(self, request):
        """
            CREATES A NEW SUGGESTION
        """
        form = ListSuggestionForm(request.POST)
        if form.is_valid():
            ls = self._create_or_update(request, form)
            return self._render(
                        request = request,
                        template = 'lists/listsuggestion_detail',
                        context = {
                                   'list': ls,
                                   },
                        status = 200)
        return self._badrequest(request, {'msg': 'invalid id'})
        
    @login_required
    def update(self, request, id):
        """
            UPDATE A EXISTING SUGGESTION
        """
        try:
            ls = ListSuggestion.objects.get(pk=id, user=request.user)
        except ListSuggestion.DoesNotExist:
            return self._notfound(request)
        form = ListSuggestionForm(request.POST, instance=ls)
        if form.is_valid():
            ls = self._create_or_update(request, form)
            return self._render(
                                request = request,
                                template = 'lists/listsuggestion_detail',
                                context = {
                                           'list': ls,
                                           },
                                status = 200)
        return self._badrequest(request, {'msg': 'invalid id'})
    
    @login_required
    def edit(self, request, id):
        """
            RETURNS THE FORM TO EDIT A EXISTING LISTSUGGESTION
        """
        try:
            ls = ListSuggestion.objects.get(pk=id, user=request.user)
        except ListSuggestion.DoesNotExist:
            return self._notfound(request)
        form = ListSuggestionForm(instance=suggestion)
        return self._render(
                            request = request,
                            template = 'lists/listsuggestion_new',
                            context = {
                                       'form': form,
                                       },
                            status = 200
                            )
        
    def _create_or_update(self, request, form):
        list_instances = request.POST.getlist('suggestions[]')
        list_instances_del = request.POST.getlist('suggestions_del[]')
        return form.save(user=request.user, ids = list_instances, ids_del=list_instances_del)
