#coding=utf-8

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def suggestion_edit(request, slug):
    pass


def suggestion_detail(request, slug):
    pass


@login_required
def suggestion_add(request):
    pass


def suggestions_list(request):
    pass