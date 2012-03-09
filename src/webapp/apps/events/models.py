#coding=utf-8

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.measure import D
from django.db.models import F
from django.contrib.gis.geos import Point
from django.core import serializers

from timezones.fields import LocalizedDateTimeField
from places.models import Place
from timelines.models import Timeline
from signals import suggestion_new
from webapp.site.models_utils import Visibility
from modules.voty.votablemanager import VotableManager

from funcs import INFO
from fields import AutoSlugField, PositiveCounterField


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^timezones.fields.LocalizedDateTimeField", "^fields.PositiveCounterField"])


class Event(models.Model):
    name = models.CharField(_(u"Nombre"), max_length=170)
    description = models.TextField(_(u"Descripción"), max_length=1024, blank=True)
    user = models.ForeignKey(User, verbose_name=_(u"Usuario"))
    created = LocalizedDateTimeField(_(u"Creado"), auto_now_add=True)
    modified = LocalizedDateTimeField(_(u"Modificado"), auto_now=True)
    place = models.ForeignKey(Place, verbose_name=_(u"Sitio"))
    location = models.PointField(_(u"Localización (no tocar)"), blank=True, null=True)
    date_starts = LocalizedDateTimeField(_(u"Fecha finalización"), blank=True, null=True)
    date_ends = LocalizedDateTimeField(_(u"Fecha finalización"), blank=True, null=True)
    done = models.BooleanField(_(u"Finalizado"), default=False)
    
    class Meta:
        abstract = True
        ordering = ['name', 'created', 'modified']
        
    def __unicode__(self):
        return unicode(self.name)


#------------------------------------------------------------------------------ 
class SuggestionManager(models.GeoManager, VotableManager):
    def create(self, **kwargs):
        to_facebook = kwargs.get('to_facebook', False)
        to_twitter = kwargs.get('to_twitter', False)
        if 'to_facebook' in kwargs:
            del kwargs['to_facebook']
        if 'to_twitter' in kwargs:
            del kwargs['to_twitter']
        obj = super(self.__class__, self).create(**kwargs)
        suggestion_new.send(sender=obj.__class__, instance=obj, created = True, to_facebook=to_facebook, to_twitter=to_twitter)
        INFO("SUGERENCIA: creada nueva sugerencia %s %s" % (obj.id, obj.name))
        return obj
        
    def get_backpack(self, follower):
        return self.get_query_set().filter(followers__user=follower).select_related('user',
                                                                    'place__city')

    def toggle_follower(self, follower, suggestion):
        suggestion_type = ContentType.objects.get_for_model(suggestion)
        q = EventFollower.objects.filter(user = follower, 
                                         event_c_type = suggestion_type,
                                         event_id = suggestion.id)
        if q.exists():
            q.delete()
            return False
        else:
            EventFollower.objects.create(event=suggestion, user=follower)
            return True
        return None
    
    def set_followers(self, suggestion, value=1):
        return self.get_query_set()._set_counter(suggestion=suggestion, counter='counter_followers', value=value)
    
    def _set_counter(self, suggestion, counter, value=1):
        return self.get_query_set().filter(
                                           pk = suggestion.pk
                                           ).update(
                                                    **{counter: models.F(counter) + value}
                                                    )
                           
    def nearest_to(self, lat, lon, accuracy=100):
        p = Point(float(lon), float(lat))
        return self.nearest_to_point(p, accuracy = accuracy)
    
    def nearest_to_point(self, point, accuracy=100):
        return self.get_query_set().filter(location__distance_lte=(point, D(m=accuracy))
                                           ).select_related('user', 'place__city').distance(point).order_by('distance')
                                           

        

class Suggestion(Event, Visibility):
    slug = AutoSlugField(populate_from=['name', 'place'], max_length = 50, unique=True)
    _short_url = models.URLField(_(u"Atajo en vavag"), blank=True, default='')
    counter_followers = PositiveCounterField(_(u"Contador de seguidores"),
                                            default=0,
                                            blank=True
                                            )
    followers = generic.GenericRelation('events.EventFollower',
                                        content_type_field='event_c_type',
                                        object_id_field='event_id')
    
    objects = SuggestionManager()
    
    class Meta:
        verbose_name = _(u"Sugerencia")
        verbose_name_plural = _(u"Sugerencias")
        
    @models.permalink
    def get_absolute_url(self):
        return ('events_suggestion_detail', (), { 'slug': self.slug })
    
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
                self._short_url = ''
                return 'http://%s%s' % (current_site.domain, self.get_absolute_url())
        return self._short_url
    
    def delete(self):
        from django.conf import settings
        suggestion_c_type = ContentType.objects.get_for_model(self)
        if self.user_id == settings.GEOREMINDME_USER_ID:
            eventfollowers = EventFollower.objects.filter(event_c_type__pk = suggestion_c_type.id,
                                                          event_id = self.id)
            for e in eventfollowers:
                e.delete()
            super(self.__class__, self).delete()
        
        timeline = Timeline.objects.filter(user_id = self.user_id,
                                content_type__pk = suggestion_c_type.id,
                                object_id = self.id)
        for t in timeline:
            t.delete()
        self.user_id = settings.GEOREMINDME_USER_ID
        self.save()
        
    @classmethod
    def serialize_to_json(cls, q, **kwargs):
        if not 'fields' in kwargs:
            kwargs['fields']=['description', 'name', 'place', 'user','distance']
        else:
            if kwargs['fields'] == ['allfields']:
                del kwargs['fields']
        json_serializer = serializers.get_serializer("json")()
        data = json_serializer.serialize(q, 
                                     ensure_ascii=kwargs.pop("ensure_ascii", False), 
                                     use_natural_keys=kwargs.pop("use_natural_keys", True),
                                     **kwargs)
        return data
    
    def natural_key(self):
        return [self.pk, self.name, self.place]
    natural_key.dependencies = ['places.Place']
                                     

#------------------------------------------------------------------------------ 
class EventFollower(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u"Usuario"),
                             related_name="events_followed")
    event_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _(u"Tipo de evento seguido"),
                                        related_name = "+")
    event_id = models.PositiveIntegerField(_(u"Identificador del evento seguido"))
    event = generic.GenericForeignKey('event_c_type', 'event_id',) # clave generica para cualquier modelo
    done = models.BooleanField(_(u"Hecho"), default=False)
    created = LocalizedDateTimeField(_(u"Creado"), auto_now_add=True)
    modified = LocalizedDateTimeField(_(u"Modificado"), auto_now=True)
    
    class Meta:
        get_latest_by = "-created"
        unique_together = (("user", "event_c_type", "event_id"),)
        verbose_name = _(u"Seguimiento de evento")
        verbose_name_plural = _(u"Seguimientos de eventos")
        
    def __unicode__(self):
        return u"%s - %s - %s" % (self.user, self.event, self.created)
    
    def delete(self, *args, **kwargs):
        timelines = Timeline.objects.filter(user__pk = self.user_id,
                                           content_type = self.event_c_type_id,
                                           object_id = self.event_id
                                           )
        for t in timelines:
            t.delete()
        super(self.__class__, self).delete(*args, **kwargs)
    
    
#===========================================================================
# Traduccion de modelos
#===========================================================================
from datatrans.utils import register
class SuggestionTranslation(object):
    fields = ('name', 'description')


#register(Suggestion, SuggestionTranslation)
