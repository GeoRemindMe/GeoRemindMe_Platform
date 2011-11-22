#coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from fields import AutoSlugField
from timezones.fields import LocalizedDateTimeField
from places.models import Place
from signals import suggestion_new
from webapp.site.models_utils import Visibility
from webapp.site.funcs import INFO


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^timezones.fields.LocalizedDateTimeField"])

class Event(models.Model):
    name = models.CharField(_(u"Nombre"), max_length=170)
    description = models.TextField(_(u"Descripción"), max_length=1024, blank=True)
    user = models.ForeignKey(User, verbose_name=_(u"Usuario"))
    created = LocalizedDateTimeField(_(u"Creado"), auto_now_add=True)
    modified = LocalizedDateTimeField(_(u"Modificado"), auto_now=True)
    place = models.ForeignKey(Place, verbose_name=_(u"Sitio"))
    date_starts = LocalizedDateTimeField(_(u"Fecha finalización"), blank=True, null=True)
    date_ends = LocalizedDateTimeField(_(u"Fecha finalización"), blank=True, null=True)
    done = models.BooleanField(_(u"Finalizado"), default=False)
    
    class Meta:
        abstract = True
        ordering = ['name', 'created', 'modified']
        
    def __unicode__(self):
        return unicode(self.name)


#------------------------------------------------------------------------------ 
class SuggestionManager(models.Manager):
    def create(self, **kwargs):
        to_facebook = kwargs.get('to_facebook', False)
        to_twitter = kwargs.get('to_twitter', False)
        if 'to_facebook' in kwargs:
            del kwargs['to_facebook']
        if 'to_twitter' in kwargs:
            del kwargs['to_twitter']
        obj = super(self.__class__, self).create(**kwargs)
        EventFollower.objects.create(event=obj, user=obj.user)
        suggestion_new.send(sender=obj, to_facebook=to_facebook, to_twitter=to_twitter)
        INFO("SUGERENCIA: creada nueva sugerencia %s %s" % (obj.id, obj.name))
        return obj
        
    def get_suggestions_by_follower(self, follower):
        ids = EventFollower.objects.filter(user=follower.id).values_list('event_id', flat=True)
        return Suggestion.objects.filter(id__in=ids).select_related('place')


class Suggestion(Event, Visibility):
    slug = AutoSlugField(populate_from=['name', 'place'], max_length = 50, unique=True)
    _short_url = models.URLField(_(u"Web"), blank=True, default='')
    
    
    objects = SuggestionManager()
    
    class Meta:
        verbose_name = _(u"Sugerencia")
        verbose_name_plural = _(u"Sugerencias")
        
    @models.permalink
    def get_absolute_url(self):
        return ('suggestions_suggestion_detail', (), { 'slug': self.slug })
    
    @property
    def short_url(self):
        if self._short_url == '':
            from django.contrib.sites.models import Site
            from libs.vavag import VavagRequest
            from django.conf import settings        
            try:
                current_site = Site.objects.get_current()
                client = VavagRequest(settings.VAVAG_PASSWORD['user'], settings.VAVAG_PASSWORD['key'])
                
                response = client.set_pack('http://%s%s' % (current_site.domain, self.get_absolute_url()))
                self._short_url = response['packUrl']
                self.save()
            except Exception:
                self._short_url = None
                return 'http://%s%s' % (current_site.domain, self.get_absolute_url())
        return self._short_url
        

#------------------------------------------------------------------------------ 
class EventFollower(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u"Usuario"),
                             related_name="events_followed")
    event_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _(u"Tipo de evento seguido"),
                                        related_name = "event_followers")
    event_id = models.PositiveIntegerField(_(u"Identificador del evento seguido"))
    event = generic.GenericForeignKey('event_c_type', 'event_id',) # clave generica para cualquier modelo
    done = models.BooleanField(_(u"Hecho"), default=False)
    created = LocalizedDateTimeField(_(u"Creado"), auto_now_add=True)
    modified = LocalizedDateTimeField(_(u"Modificado"), auto_now=True)
    
    class Meta:
        get_latest_by = "created"
        ordering = ['-created']
        unique_together = (("user", "event_c_type", "event_id"),)
        verbose_name = _(u"Seguimiento de evento")
        verbose_name_plural = _(u"Seguimientos de eventos")
        
    def __unicode__(self):
        return u"%s - %s - %s" % (self.user, self.event, self.created)
    
    
#===========================================================================
# Traduccion de modelos
#===========================================================================
from datatrans.utils import register
class SuggestionTranslation(object):
    fields = ('name', 'description')


register(Suggestion, SuggestionTranslation)
