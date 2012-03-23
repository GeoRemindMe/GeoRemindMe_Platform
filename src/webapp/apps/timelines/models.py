#coding=utf-8


from django.db import models, transaction
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.db.models import F, Q

from modules.timezones.fields import LocalizedDateTimeField
from modules.efficient.utils import get_generic_relations
from modules.voty.votablemanager import VotableManager
from modules.voty.models import Vote


class NotificationSettings(models.Model):
    TIME_CHOICES = (
           (0, _(u'Nunca')),
           (1, _(u'Inmediato')),
           (2, _(u'Diario')),
           (3, _(u'Semanal')),
           (4, _(u'Mensual')),
    )
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_(u'usuario'),
                                )
    
    notification_invitation = models.PositiveSmallIntegerField(choices=TIME_CHOICES,
                                               default=1,
                                               verbose_name=_(u"Notificar invitaciones")
                                              )
    notification_suggestion = models.PositiveSmallIntegerField(choices=TIME_CHOICES,
                                               default=1,
                                               verbose_name=_(u"Notificar cambios tus sugerencias")
                                              )
    notification_account = models.PositiveSmallIntegerField(choices=TIME_CHOICES,
                                               default=1,
                                               verbose_name=_(u"Notificar cuando te siguen")
                                              )

    class Meta:
        verbose_name = _('Configuracion de notificaciones')
        verbose_name_plural = _('Configuraciones de notificaciones')


#------------------------------------------------------------------------------ 
class FollowerManager(models.Manager):
    def is_follower(self, follower, followee, **kwargs):
        if follower.__eq__(followee):
            return True
        follower_type = ContentType.objects.get_for_model(follower)
        followee_type = ContentType.objects.get_for_model(followee)
        return self.filter(follower_id=follower.id,  
                        follower_c_type=follower_type,
                        followee_id=followee.id, 
                        followee_c_type=followee_type).exists()
        
    def toggle_follower(self, follower, followee, **kwargs):
        if follower.__eq__(followee):
            return None
        follower_type = ContentType.objects.get_for_model(follower)
        followee_type = ContentType.objects.get_for_model(followee)
        
        q = self.get_query_set().filter(follower_id=follower.id, follower_c_type=follower_type,
                                      followee_id=followee.id, followee_c_type=followee_type
                                      )
        if q.exists():
                q.delete()
                return False
        else:
                self.create(follower=follower, followee=followee, **kwargs)
                return True
        return None
    
    def get_by_follower(self, follower, type_filter=None):
        follower_type = ContentType.objects.get_for_model(follower)
        if type_filter is not None:
            followee_type = ContentType.objects.get_for_model(type_filter)
            ids = self.get_query_set().filter(follower_id=follower.id,
                               follower_c_type=follower_type,
                               followee_c_type=followee_type).values_list('followee_id', flat=True)
            return User.objects.filter(id__in=ids).select_related('profile')
        else:
            ids = self.get_query_set().filter(follower_id=follower.id,
                               follower_c_type=follower_type).values_list('followee_id', flat=True)
            return User.objects.filter(id__in=ids).select_related('profile')
                                
    def get_by_followee(self, followee, type_filter=None):
        followee_type = ContentType.objects.get_for_model(followee)
        if type_filter is not None:
            followee_type = ContentType.objects.get_for_model(type_filter)
            ids = self.filter(followee_id=followee.id,
                               followee_c_type=followee_type,
                               follower_c_type=followee_type).values_list('follower_id', flat=True)
            return User.objects.filter(id__in=ids).select_related('profile')
        else:
            ids = self.filter(followee_id=followee.id,
                               followee_c_type=followee_type).values_list('follower_id', flat=True)
            return User.objects.filter(pk__in=ids).select_related('profile')
        

class Follower(models.Model):
    follower_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _(u"Tipo de objeto seguidor"),
                                        related_name = "followings")
    follower_id = models.IntegerField(_(u"Identificador del seguidor"))
    follower = generic.GenericForeignKey('follower_c_type', 'follower_id',) # clave generica para cualquier modelo

    followee_c_type = models.ForeignKey(ContentType,
                                     verbose_name = _(u"Tipo de objeto seguido"),
                                     related_name = "followers")
    followee_id = models.IntegerField(_(u"Identificador del seguido"))
    followee = generic.GenericForeignKey('followee_c_type', 'followee_id',) # clave generica para cualquier modelo
    
    modified = LocalizedDateTimeField(_(u"Modificado"),
                                      auto_now=True)
    created = LocalizedDateTimeField(auto_now_add=True)
    objects = FollowerManager()
    
    class Meta:
        get_latest_by = "created"
        unique_together = (("follower_c_type", "follower_id", "followee_c_type", "followee_id"),)
        verbose_name = _(u"Seguimiento")
        verbose_name_plural = _(u"Seguimientos")
        
    def __unicode__(self):
        return "%s - %s - %s" % (self.follower.username, self.followee.username, self.created)
    
    def delete(self, *args, **kwargs):
        timeline = Timeline.objects.filter(user_id = self.follower_id, 
                                           content_type = self.followee_c_type, 
                                           object_id = self.followe_id,
                                           msg_id = self.msg_id)
        for t in timeline:
            t.delete()
        super(self.__class__, self).delete()


#------------------------------------------------------------------------------ 
class TimelineManager(VotableManager):
    def add_timeline(self, actor, msg_id, objetive, visible, result=None, **kwargs):
        if result is not None:
            timeline = self.create(
                                actor = actor,
                                msg_id = msg_id,
                                objetive = objetive,
                                visible = visible,
                                result=result,
                                **kwargs
                                )
        else:
            timeline = self.create(
                                actor = actor,
                                msg_id = msg_id,
                                objetive = objetive,
                                visible = visible,
                                **kwargs
                                )
        TimelineFollower(timeline = timeline,
                         follower = actor
                         )
        return timeline
        
    def del_all_timelines(self, actor, msg_id, objetive):
        objetive_type = ContentType.objects.get_for_model(objetive)
        actor_type = ContentType.objects.get_for_model(actor)
        return self.get_quey_set().filter(actor_c_type = actor_type, actor_id = actor.id,
                                          msg_id = msg_id,
                                          objetive_c_type = objetive_type,
                                          objective_id = objetive.id
                                          ).delete()

    def get_by_objetive(self, objetive, visible=True):
        """
            Obtiene el timeline publico perteneciente a un objeto
            
            :param instance: objeto a buscar
            :type instance: Cualquiera
            :param visible: Solo si el timeline es publico o todo
            :type visible: :class:`Boolean`
            
            :returns: Iterator
            
        """
        q= objetive.objetive_timelines.filter(visible=visible).order_by('-modified')
        return get_generic_relations(q, ['actor', 'objetive', 'result'])
    
    def get_by_user(self, user, visible=True, all=False):
        """
            Obtiene el timeline publico o privado de un usuario
            
            :param user: Usuario a buscar
            :type user: :class:`django.contrib.auth.User`
            :param visible: Solo si el timeline es publico o todo
            :type visible: :class:`Boolean`
            
        """
        if isinstance(user, basestring):
            actor = User.objects.get(username = user.lower())
        else:
            actor = user
        
        q = actor.actor_timelines.get_query_set().order_by('-modified')
        if not all: # todo el timeline, visible y no visible
            q = q.filter(visible=visible)
        return get_generic_relations(q, ['actor', 'objetive', 'result'])
    
    def get_chronology(self, user):
        """
            Obtiene la cronologia de un usuario (su timeline, mas el de seguidos)
            
            :param user: Usuario a buscar
            :type user: :class:`django.contrib.auth.User`
        """
        if isinstance(user, basestring):
            actor = User.objects.get(username = user.lower())
        else:
            actor = user
        actor_ct = ContentType.objects.get_for_model(actor)

        q = self.has_voted(user).filter(timelinefollowers__follower_c_type = actor_ct,
                                       timelinefollowers__follower_id = actor.id).order_by('-modified')[:10]
        return get_generic_relations(q, ['actor', 'objetive', 'result'])
    
    def has_voted(self, user):
        if not user.is_authenticated():
            return self.get_query_set()
        table = Vote._meta.db_table
        table2 = self.model._meta.db_table
        select = 'SELECT True FROM %s' % table
        where1 = 'WHERE ' + table + '.user_id = %s' 
        where2 = 'AND ' + table + '.target_id = ' + table2 + '.objetive_id'
        where3 = 'AND ' + table + '.target_c_type_id = ' + table2 + '.objetive_c_type_id'
        return self.get_query_set().extra(
                                          select={'has_voted':" ".join((select, where1, where2, where3))},
                                          select_params=[user.id]
                                          )
        

class Timeline(models.Model):
    ## 0: _('Welcome to GeoRemindMe you can share your public profile: \
    ## <a href="http://www.georemindme.com/user/%(username)s/">\
    ## http://www.georemindme.com/user/%(username)s/</a>') %{
    ## 'username':self.user.username,
    ## },
    ## 1: _('Now, you can log with your Google account'),
    ## 2: _('Now, you can log from Facebook and from <a href="http://www.georemindme.com" target="_blank">www.georemindme.com</a>'),
    ## 3: _('Now, you can log with your Twitter account'),
    ##
    ## #User messages
    ## 100: _('You are now following <a href="%(profile_url)s">%(username)s</a>') % {
    ## 'profile_url':self.user.get_absolute_url(),
    ## 'username':self.instance
    ## },
    ## 101: _('<a href="%(profile_url)s">%(username)s</a> is now following you') % {
    ## 'profile_url':self.user.get_absolute_url(),
    ## 'username':self.instance
    ## },
    ## 102: _('You are no longer following <a href="%(profile_url)s">%(username)s</a> anymore') % {
    ## 'profile_url':self.user.get_absolute_url(),
    ## 'username':self.instance
    ## },
    ## 110: _('You invited %s to:') % self.instance,
    ## 111: _('%s invited you to %s') % (self.instance, self.instance),
    ## 112: _('%s accepted your invitation to %s') % (self.user, self.instance),
    ## 113: _('%s rejected your invitation to %s') % (self.user, self.instance),
    ## 120: _('<a href="%(profile_url)s">%(username)s</a> ha hecho un comentario en la sugerencia: <br><a href="/fb/suggestion/%(suggestion_id)s/">%(suggestion)s</a>') % {
    ## 'profile_url':self.user.get_absolute_url(),
    ## 'username':self.user,
    ## 'suggestion':self.instance,
    ## 'suggestion_id':self.instance,
    ## },
    ## 125: _('likes a comment: %s') % self.instance,
    ## 150: _('New user list created: %s') % self.instance,
    ## 151: _('User list modified: %s') % self.instance,
    ## 152: _('User list removed: %s') % self.instance,
    ##
    ## #Alerts
    ## 200: _('New alert: %s') % self.instance,
    ## 201: _('Alert modified: %s') % self.instance,
    ## 202: _('Alert deleted: %s') % self.instance,
    ## 203: _('Alert done: %s') % self.instance,
    ##
    ## #Alerts lists
    ## 250: _('New alert list created: %s') % self.instance,
    ## 251: _('Alert list modified: %s') % self.instance,
    ## 252: _('Alert list removed: %s') % self.instance,
    ##
    ## #Suggestions
    ## 300: _('<a href="/fb%(url)s">%(username)s</a> sugiere:<br> %(message)s') % {
    ## 'url':self.user.get_absolute_url(),
    ## 'username':self.user.username,
    ## 'message':self.instance
    ## },
    ## 301: _('Suggestion modified: %s') % self.instance,
    ## 302: _('Suggestion removed: %s') % self.instance,
    ## 303: _('You are following: %s') % self.instance,
    ## 304: _('You stopped following: %s') % self.instance,
    ## 305: _('likes a suggestions: %s') % self.instance,
    ## 320: _('New alert: %s') % self.instance,
    ## 321: _('Alert modified: %s') % self.instance,
    ## 322: _('Alert deleted: %s') % self.instance,
    ## 323: _('Alert done: %s') % self.instance,
    ##
    ## #Suggestions list
    ## 350: _('New suggestions list created: %s') % self.instance,
    ## 351: _('Suggestions list modified: %s') % self.instance,
    ## 352: _('Suggestion list removed: %s') % self.instance,
    ## 353: _('You are following: %s') % self.instance,
    ## 354: _('You are not following %s anymore') % self.instance,
    ##
    ## #Places
    ## 400: _('New private place: %s') % self.instance,
    ## 401: _('Private place modified: %s') % self.instance,
    ## 402: _('Private place deleted: %s') % self.instance,
    ## 450: _('New public place: %s') % self.instance,
    ## 451: _('Public place modified: %s') % self.instance,
    ## 452: _('Public place deleted: %s') % self.instance,
    ##
    actor_c_type = models.ForeignKey(ContentType,
                                    verbose_name = _(u"Tipo de objeto actor"),
                                    related_name='+'
                                    )
    actor_id = models.IntegerField(_(u"Identificador del actor"))
    actor = generic.GenericForeignKey('actor_c_type', 'actor_id',) # clave generica para cualquier modelo
    
    msg_id = models.PositiveSmallIntegerField(_(u"Tipo de mensaje"))
    
    objetive_c_type = models.ForeignKey(ContentType,
                                    verbose_name = _(u"Tipo de objeto objetivo"),
                                    related_name='+'
                                    )
    objetive_id = models.IntegerField(_(u"Identificador del objetivo"))
    objetive = generic.GenericForeignKey('objetive_c_type', 'objetive_id',) # clave generica para cualquier modelo
    
    result_c_type = models.ForeignKey(ContentType,
                                    verbose_name = _(u"Tipo de objeto resultado"),
                                    related_name='+',
                                    null=True,
                                    blank=True
                                    )
    result_id = models.IntegerField(_(u"Identificador del resultado"), 
                                    null=True,
                                    blank=True)
    result = generic.GenericForeignKey('result_c_type', 'result_id',) # clave generica para cualquier modelo
    
    message = models.TextField(_(u"Texto extra"), blank=True) 
    visible = models.BooleanField(_(u"Visible en perfil publico"),
                                  default=True,
                                  )
    created = LocalizedDateTimeField(_(u"Creado"),
                                   auto_now_add=True)
    modified = LocalizedDateTimeField(_(u"Modificado"),
                                      auto_now=True)
    
    objects = TimelineManager()
    
    class Meta:
        get_latest_by = "created"
        verbose_name = _(u"Timeline")
        verbose_name_plural = _(u"Timelines")
        
    def __unicode__(self):
        return "%s - %d - %s" % (self.actor, self.id, self.modified)
    
    def delete(self, *args, **kwargs):
        TimelineFollower.objects.filter(timeline=self).delete()
        TimelineNotification.objects.filter(timeline=self).delete()
        super(self.__class__, self).delete()
        

#------------------------------------------------------------------------------ 


class TimelineFollowerManager(models.Manager):
    @transaction.commit_manually
    def bulk_create(self, instances):
        # TODO : EN VERSION DE DESARROLLO DE DJANGO, YA EXISTE, INSERTA OBJETOS POR LOTES
        try:
            for instance in instances:
                instance.save()
        except:
            transaction.rollback()
        else:
            transaction.commit()
        

class TimelineFollower(models.Model):
    timeline = models.ForeignKey(Timeline,
                                 verbose_name = _(u"Timeline follower"),
                                 related_name = "timelinefollowers"
                                 )
    
    follower_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _(u"Tipo de objeto seguidor"),
                                        related_name = "+")
    follower_id = models.IntegerField(_(u"Identificador del seguidor"))
    follower = generic.GenericForeignKey('follower_c_type', 'follower_id',) # clave generica para cualquier modelo
    
    created = LocalizedDateTimeField(auto_now_add=True)
    modified = LocalizedDateTimeField(_(u"Modificado"),
                                      auto_now=True)
    objects = TimelineFollowerManager()
    
    class Meta:
        get_latest_by = "created"
        unique_together = (("timeline", "follower_c_type", "follower_id"),)
        verbose_name = _(u"Seguidor de Timeline")
        verbose_name_plural = _(u"Seguidores de Timelines")
        
    def __unicode__(self):
        return "%s - %d - %s" % (self.follower, self.timeline_id, self.created)
    


class TimelineNotificationManager(models.Manager):
    def add_notification(self, timeline, user=None):
        if user is None:
            user = timeline.instance.user   
        obj = self.create(timeline = timeline,
                           actor = user
                        )
        UserProfile.objects.filter(
                                   user = user
                                   ).update(
                                            counter_notifications = F('counter_notifications') + 1
                                            )
        return obj

    def get_by_user(self, user):
        if isinstance(user, basestring):
            actor = User.objects.get(username = user.lower())
        else:
            actor = user
        actor_ct = ContentType.objects.get_for_model(actor)

        q = Timeline.objects.filter(
                                       timelinenotifications__actor_c_type = actor_ct,
                                       timelinenotifications__actor_id = actor.id,
                                       ).order_by('created')
        return get_generic_relations(q, ['actor', 'objetive', 'result'])


class TimelineNotification(models.Model):
    timeline = models.ForeignKey(Timeline,
                                 verbose_name = _(u"Timeline notified"),
                                 related_name = "timelinenotifications"
                                 )
    
    actor_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _(u"Tipo de objeto seguidor"),
                                        related_name = "timelinenotifications")
    actor_id = models.IntegerField(_(u"Identificador del seguidor"))
    actor = generic.GenericForeignKey('actor_c_type', 'actor_id',) # clave generica para cualquier modelo
    
    created = LocalizedDateTimeField(auto_now_add=True)
    modified = LocalizedDateTimeField(_(u"Modificado"),
                                      auto_now=True)
    
    objects = TimelineNotificationManager()
    
    class Meta:
        unique_together = (("timeline", "actor_c_type", "actor_id"),) 
        get_latest_by = "created"
        verbose_name = _(u"Notificacion de Timeline")
        verbose_name_plural = _(u"Notificaciones de Timelines")
        
    def __unicode__(self):
        return "%s - %d - %s" % (self.actor, self.timeline_id, self.created)
    
try:
    # south fails migrating with this code :)
    GenericModels = ['auth.User', 'events.Suggestion', 'places.Place', 'events.EventFollower']
    # from django-activity-stream
    from django.db.models import get_model
    for model in GenericModels:
        model = get_model(*model.split('.'))
        opts = model._meta
        for field in ('actor', 'objetive', 'result'):
            generic.GenericRelation(Timeline, 
                                    content_type_field="%s_c_type" % field,
                                    object_id_field='%s_id' % field,
                                    related_name='timelines_with_%s_%s_as_%s' % ( 
                                                                                 opts.app_label,
                                                                                 opts.module_name,
                                                                                 field)
                                    ).contribute_to_class(model, '%s_timelines' % field)
            setattr(Timeline, 'timelines_with_%s_%s_as_%s' % (opts.app_label,
                                                              opts.module_name,
                                                           field), None)
            
        # south fails migrating with this code :)
    GenericModelsFollowers = ['auth.User']
    # from django-activity-stream
    
    for model in GenericModelsFollowers:
        model = get_model(*model.split('.'))
        opts = model._meta
        for field in ('follower', 'followee',):
            generic.GenericRelation(Follower, 
                                    content_type_field="%s_c_type" % field,
                                    object_id_field='%s_id' % field,
                                    related_name='users_as_%s' % (
                                                               field)
                                    ).contribute_to_class(model, '%ss' % field)
            setattr(Follower, 'users_as_%s' % (field), None)
        generic.GenericRelation(TimelineFollower, 
                                    content_type_field="follower_c_type",
                                    object_id_field='follwer_id',
                                    related_name='timelinesfollowers_as_follower'
                                    ).contribute_to_class(model, 'timelinefollowees')
        setattr(TimelineFollower, 'timelinefollowers' % (field), None)
            
                
    
except:
    pass
from profiles.models import UserProfile