#coding=utf-8

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def place_edit(request, slug):
    pass


def place_detail(request, slug):
    pass


@login_required
def place_add(request):
    pass


def places_list(request):
    pass