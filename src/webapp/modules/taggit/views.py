from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.datastructures import MultiValueDictKeyError

from taggit.models import TaggedItem, Tag

def tagged_object_list(request, slug, queryset, **kwargs):
    if callable(queryset):
        queryset = queryset()
    tag = get_object_or_404(Tag, slug=slug)
    qs = queryset.filter(pk__in=TaggedItem.objects.filter(
        tag=tag, content_type=ContentType.objects.get_for_model(queryset.model)
    ).values_list("object_id", flat=True))
    if "extra_context" not in kwargs:
        kwargs["extra_context"] = {}
    kwargs["extra_context"]["tag"] = tag
    return object_list(request, qs, **kwargs)

def list_tags(request):
    try:
        tags = Tag.objects.filter(name__icontains=request.GET['q']).values_list('name', flat=True)
        data = [{'value': t, 'name': t} for t in tags]
    except MultiValueDictKeyError:
        data = []
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')
