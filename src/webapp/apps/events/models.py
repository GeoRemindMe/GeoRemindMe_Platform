#coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from fields import AutoSlugField
from places.models import Place

class Event(models.Model):
    name = models.CharField(_(u"Nombre"), max_length=170)
    description = models.TextField(_(u"Descripción"), max_length=1024)
    user = models.ForeignKey(User, verbose_name=_(u"Usuario"))
    created = models.DateTimeField(_(u"Creado"), auto_now_add=True)
    modified = models.DateTimeField(_(u"Modificado"), auto_now=True)
    place = models.ForeignKey(Place, verbose_name=_(u"Sitio"))
    date_starts = models.DateTimeField(_(u"Fecha finalización"), blank=True)
    date_ends = models.DateTimeField(_(u"Fecha finalización"), blank=True)
    done = models.BooleanField(_(u"Finalizado"), default=False)
    
    class Meta:
        abstract = True
        ordering = ['name', 'created', 'modified']
        
    def __unicode__(self):
        return self.name


class Suggestion(Event):
    slug = AutoSlugField(populate_from=['name', 'place'], max_length = 50, unique=True)
    
    class Meta:
        verbose_name = _(u"Sugerencia")
        verbose_name_plural = _(u"Sugerencias")


class EventFollower(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u"Usuario"),
                             related_name="events_followed")
    event_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _(u"Tipo de evento seguido"),
                                        related_name = "event_followers")
    event_id = models.PositiveIntegerField(_(u"Identificador del evento seguido"))
    event = generic.GenericForeignKey('event_c_type', 'event_id',) # clave generica para cualquier modelo
    done = models.BooleanField(_(u"Hecho"), default=False)
    created = models.DateTimeField(_(u"Creado"), auto_now_add=True)
    modified = models.DateTimeField(_(u"Modificado"), auto_now=True)
    
    class Meta:
        get_latest_by = "created"
        ordering = ['-created']
        unique_together = (("user", "event_c_type", "event_id"),)
        verbose_name = _(u"Seguimiento de evento")
        verbose_name_plural = _(u"Seguimientos de eventos")
        
    def __unicode__(self):
        return "%s - %s - %s" % (self.user, self.event, self.created)
    
    
#===========================================================================
# Traduccion de modelos
#===========================================================================
from datatrans.utils import register
class SuggestionTranslation(object):
    fields = ('name', 'description')


register(Suggestion, SuggestionTranslation)
