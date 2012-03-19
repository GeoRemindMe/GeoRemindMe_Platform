#coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from modules.timezones.fields import LocalizedDateTimeField
from webapp.site.models_utils import Visibility
from webapp.site.funcs import INFO

from timelines.models import Timeline
from events.models import Suggestion
from fields import PositiveCounterField
from signals import * #@UnusedWildImport


class ListGenericManager(models.Model):
    def toggle_follower(self, follower, listobj):
        list_type = ContentType.objects.get_for_model(listobj)
        q = ListFollower.objects.filter(user = follower,
                                         event_c_type = list_type,
                                         event_id = list.id)
        if q.exists():
            q.delete()
            return False
        else:
            ListFollower.objects.create(event=listobj, user=follower)
            return True
        return None


class ListGeneric(models.Model):
    name = models.CharField(_(u"Nombre"), max_length=128)
    description = models.TextField(_(u"Descripcion"))
    user = models.ForeignKey('auth.User', verbose_name=_(u"Usuario"))
    
    created = LocalizedDateTimeField(_(u"Creado"), auto_now_add=True)
    modified = LocalizedDateTimeField(_(u"Modificado"), auto_now=True)
    
    
    class Meta:
        abstract = True
    

#------------------------------------------------------------------------------

class ListSuggestionManager(models.Manager):
    def create(self, *args, **kwargs):
        to_facebook = kwargs.get('to_facebook', False)
        to_twitter = kwargs.get('to_twitter', False)
        if 'to_facebook' in kwargs:
            del kwargs['to_facebook']
        if 'to_twitter' in kwargs:
            del kwargs['to_twitter']
        obj = super(self.__class__, self).create(*args, **kwargs)
        list_new.send(sender=obj.__class__, instance=obj, created=True, to_facebook=to_facebook, to_twitter=to_twitter)
        INFO("LISTA SUGERENCIAS: creada nueva lista %s %s" % (obj.id, obj.name))
        return obj
    
    def get_by_follower(self, follower):
        return self.get_query_set().filter(followers__user=follower).select_related('user')

    def create_from_ids(self, *args, **kwargs):
        if 'suggestions' in kwargs:
            not_repeated = set(kwargs['suggestions'])
            kwargs['suggestions'] = Suggestion.objects.filter(pk__in=not_repeated)
            return self.create(*args, **kwargs)
        raise KeyError
    
    def set_followers(self, listobj, value=1):
        return self._set_counter(listobj=listobj, counter='counter_followers', value=value)
    
    def _set_counter(self, listobj, counter, value=1):
        return self.filter(
                            pk = listobj.pk
                           ).update(
                                    **{counter: models.F(counter) + value}
                                    )


class ListSuggestion(ListGeneric, Visibility):
    suggestions = models.ManyToManyField(Suggestion, 
                                         verbose_name=_(u"Sugerencias en la lista"),
                                         through='SuggestionInList')
    _short_url = models.URLField(_(u"Atajo en vavag"), blank=True, default='')
    counter_followers = PositiveCounterField(_(u"Contador de seguidores"),
                                            default=0,
                                            blank=True
                                            )
    followers = generic.GenericRelation('lists.ListFollower',
                                        content_type_field='list_c_type',
                                        object_id_field='list_id')
    
    objects = ListSuggestionManager()
    
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
    
    def set_suggestions(self, ids=[], commit = False):
        ids_set = set(ids)
        suggestions = Suggestion.objects.filter(pk__in = ids_set)
        self.suggestions = suggestions
        if commit:
            self.save()

    @models.permalink
    def get_absolute_url(self):
        return ('lists_suggestion_detail', (), { 'id': self.id })


class SuggestionInList(models.Model):
    listsuggestion = models.ForeignKey(ListSuggestion)
    suggestion = models.ForeignKey(Suggestion)
    created = LocalizedDateTimeField(_(u"Creado"), auto_now_add=True)
    modified = LocalizedDateTimeField(_(u"Modificado"), auto_now=True)
    
    class Meta:
        unique_together = ('listsuggestion','suggestion')


#------------------------------------------------------------------------------
class ListFollower(models.Model):
    user = models.ForeignKey('auth.User', 
                             verbose_name=_(u"Usuario"),
                             related_name="lists_followed")
    list_c_type = models.ForeignKey(ContentType,
                                    verbose_name = _(u"Tipo de lista seguido"),
                                    related_name = "list_followers")
    list_id = models.PositiveIntegerField(_(u"Identificador de la lista seguida"))
    list_instance = generic.GenericForeignKey('list_c_type', 'list_id',) # clave generica para cualquier modelo
    created = LocalizedDateTimeField(_(u"Creado"), auto_now_add=True)
    modified = LocalizedDateTimeField(_(u"Modificado"), auto_now=True)
    
    class Meta:
        get_latest_by = "created"
        unique_together = (("user", "list_c_type", "list_id"),)
        verbose_name = _(u"Seguimiento de lista")
        verbose_name_plural = _(u"Seguimientos de listas")
        
    def __unicode__(self):
        return u"%s - %s" % (self.user, self.created)
  



#from django.db import models, transaction
#from django.contrib.contenttypes import generic
#from django.contrib.contenttypes.models import ContentType
#from django.utils.translation import ugettext_lazy as _
#
#from timezones.fields import LocalizedDateTimeField
#from webapp.site.models_utils import Visibility
#from webapp.site.funcs import INFO
#from modules.efficient.utils import get_generic_relations
#
#from timelines.models import Timeline
#from events.models import Suggestion
#from fields import PositiveCounterField
#from signals import * #@UnusedWildImport
#
#
#class ListManager(models.Manager):
#    def toggle_follower(self, follower, list_obj):
#        pass
#    
#    @transaction.commit_on_success
#    def create(self, user, name, descripcion, recipients, *args, **kwargs):
#        to_facebook = kwargs.get('to_facebook', False)
#        to_twitter = kwargs.get('to_twitter', False)
#        if 'to_facebook' in kwargs:
#            del kwargs['to_facebook']
#        if 'to_twitter' in kwargs:
#            del kwargs['to_twitter']
#        list_obj = super(self.__class__,self).create(user, name, descripcion)
#        
#        if recipients:
#            recipients = set(recipients)
#            recipient_name = list_obj.list_c_type.__class__
#            recipients_pre_save = []
#            for r in recipients:
#                if recipient_name != r.__class__:
#                    raise KeyError()
#                recipients_pre_save.append(ListRecipient(user=user,
#                                                         in_list = list_obj,
#                                                         recipient = r)
#                                           )
#
#        INFO("LISTA SUGERENCIAS: creada nueva lista %s %s" % (list_obj.id, list_obj.name))
#        #list_new.send(sender=list_obj, to_facebook=to_facebook, to_twitter=to_twitter)
#        return list_obj
#    
#    def get_by_follower(self, follower, type_filter=None):
#        if type_filter is not None:
#            ct = ContentType.objects.get_for_model(type_filter)
#            q = self.filter(followers__user = follower,
#                                       recipients__recipient_c_type = ct)
#        else:
#            q = self.filter(user = follower)
#        return q # USAR PREFETCH_RELATED EN SIGUIENTE DJANGO
#        
#    def create_from_ids(self, *args, **kwargs):
#        if not 'recipients' in kwargs or not 'content_type' in kwargs:
#            raise KeyError
#        not_repeated  = set(kwargs['recipients'])
#        kwargs['recipients'] = kwargs['content_type'].objects.filter(pk__in=not_repeated)
#        return self.create(*args, **kwargs)
#    
#    def set_followers(self, listobj, value=1):
#        return self._set_counter(listobj=listobj, counter='counter_followers', value=value)
#    
#    def _set_counter(self, listobj, counter, value=1):
#        return self.filter(
#                            pk = listobj.pk
#                           ).update(
#                                    **{counter: models.F(counter) + value}
#                                )
#    
#class List(Visibility):
#    name = models.CharField(_(u"Nombre"), max_length=128)
#    description = models.TextField(_(u"Descripcion"))
#    user = models.ForeignKey('auth.User', 
#                             verbose_name=_(u"Usuario"), 
#                             related_name='+')
#    list_c_type = models.ForeignKey(ContentType,
#                                    verbose_name = _(u"Tipo de objeto de la lista"),
#                                    related_name = "+")
#    _short_url = models.URLField(_(u"Atajo en vavag"), blank=True, default='')
#    counter_followers = PositiveCounterField(_(u"Contador de seguidores"),
#                                            default=0,
#                                            blank=True
#                                            )
#    created = LocalizedDateTimeField(_(u"Creado"), auto_now_add=True)
#    modified = LocalizedDateTimeField(_(u"Modificado"), auto_now=True)
#    
#    objects = ListManager()
#    
#
#class ListRecipient(models.Model):
#    user = models.ForeignKey('auth.User', 
#                             verbose_name=_(u"Usuario"),
#                             related_name='+')
#    in_list = models.ForeignKey('lists.List',
#                                verbose_name=_(u"Lista a la que pertenece"),
#                                related_name = 'recipients')
#    recipient_c_type = models.ForeignKey(ContentType,
#                                        verbose_name = _(u"Tipo de objeto de la lista"),
#                                        related_name = "+")
#    recipient_id = models.PositiveIntegerField(_(u"Identificador del objeto"))
#    recipient = generic.GenericForeignKey('recipient_c_type', 'recipient_id',) # clave generica para cualquier modelo
#    created = LocalizedDateTimeField(_(u"Creado"), auto_now_add=True)
#    modified = LocalizedDateTimeField(_(u"Modificado"), auto_now=True)
    