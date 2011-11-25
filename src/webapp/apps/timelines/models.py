#coding=utf-8


from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from django.db import transaction

from timezones.fields import LocalizedDateTimeField
from signals import timeline_added, follower_added, follower_deleted, notification_added


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^timezones.fields.LocalizedDateTimeField"])


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
        
        q = self.filter(follower_id=follower.id, follower_c_type=follower_type,
                                  followee_id=followee.id, followee_c_type=followee_type)
        
        if q.exists():
            try:
                q.delete()
                follower_deleted.send(sender=follower, followee=followee)
                return False
            except:
                pass
            
        else:
            try:
                self.create(follower=follower, followee=followee, **kwargs)
                follower_added.send(sender=follower, followee=followee)
                return True
            except:
                pass
        return None
    
    def get_by_follower(self, follower, type_filter=None):
        follower_type = ContentType.objects.get_for_model(follower)
        if type_filter is not None:
            followee_type = ContentType.objects.get_for_model(type_filter)
            ids = self.filter(follower_id=follower.id,
                               follower_c_type=follower_type,
                               followee_c_type=followee_type).values_list('followee_id', flat=True)
            return User.objects.filter(id__in=ids).select_related('profile')
        else:
            ids = self.filter(follower_id=follower.id,
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
            return User.objects.filter(id__in=ids).select_related('profile')
        

class Follower(models.Model):
    follower_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _(u"Tipo de objeto seguidor"),
                                        related_name = "followings")
    follower_id = models.PositiveIntegerField(_(u"Identificador del seguidor"))
    follower = generic.GenericForeignKey('follower_c_type', 'follower_id',) # clave generica para cualquier modelo

    followee_c_type = models.ForeignKey(ContentType,
                                     verbose_name = _(u"Tipo de objeto seguido"),
                                     related_name = "followers")
    followee_id = models.PositiveIntegerField(_(u"Identificador del seguido"))
    followee = generic.GenericForeignKey('followee_c_type', 'followee_id',) # clave generica para cualquier modelo
    
    created = models.DateTimeField(auto_now_add=True)
    objects = FollowerManager()
    
    class Meta:
        get_latest_by = "created"
        ordering = ['-created']
        unique_together = (("follower_c_type", "follower_id", "followee_c_type", "followee_id"),)
        verbose_name = _(u"Seguimiento")
        verbose_name_plural = _(u"Seguimientos")
        
    def __unicode__(self):
        return "%s - %s - %s" % (self.follower, self.followee, self.created)
    
    def delete(self, *args, **kwargs):
        timeline = Timeline.objects.filter(user_id = self.follower_id, 
                                           content_type = self.followee_c_type, 
                                           object_id = self.followe_id,
                                           msg_id = self.msg_id)
        for t in timeline:
            t.delete()
        super(self.__class__, self).delete()


#------------------------------------------------------------------------------ 
class TimelineManager(models.Manager):
    def add_timeline(self, user, msg_id, instance, visible, **kwargs):
        timeline = self.create(user = user,
                    msg_id = msg_id,
                    instance = instance,
                    visible = visible,
                    **kwargs)
        # el usuario sigue a sus propios timelines
        TimelineFollower.objects.create(timeline=timeline, follower=user)
        timeline_added.send(sender=timeline)
        return timeline
        
    def del_all_timelines(self, user, msg_id, instance):
        instance_type = ContentType.objects.get_for_model(instance)
        return self.filter(user = user,
                    msg_id = msg_id,
                    content_type = instance_type,
                    object_id = instance.id
                    ).delete()
        
    
    def get_by_instance(self, instance, visible=True):
        """
            Obtiene el timeline publico perteneciente a un objeto
            
            :param instance: objeto a buscar
            :type instance: Cualquiera
            :param visible: Solo si el timeline es publico o todo
            :type visible: :class:`Boolean`
            
            :returns: Iterator
            
        """
        c_type = ContentType.objects.get_for_model(instance)
        return self.filter(instance_id=object.id, content_type=c_type, visible=visible).select_related(depth=1)#.iterator()
    
    def get_by_user(self, user, visible=True, all=False):
        """
            Obtiene el timeline publico o privado de un usuario
            
            :param user: Usuario a buscar
            :type user: :class:`django.contrib.auth.User`
            :param visible: Solo si el timeline es publico o todo
            :type visible: :class:`Boolean`
            
        """
        if isinstance(user, basestring):
            q = self.filter(user__username__iexact = user)
        else:
            q = self.filter(user = user)
        if not all: # todo el timeline, visible y no visible
            return q.filter(visible=visible).select_related(depth=1)#.iterator()
        else:
            return q.select_related(depth=1)#.iterator()
    
    def get_chronology(self, user):
        """
            Obtiene la cronologia de un usuario (su timeline, mas el de seguidos)
            
            :param user: Usuario a buscar
            :type user: :class:`django.contrib.auth.User`
        """
        user_type = ContentType.objects.get_for_model(user)
        queryset = self.filter(timelinefollower__follower_c_type = user_type,
                                       timelinefollower__follower_id = user.id)
        return queryset.select_related()
        generics = {}
        for item in queryset:
            generics.setdefault(item.content_type_id, set()).add(item.object_id)

        content_types = ContentType.objects.in_bulk(generics.keys())

        relations = {}
        for ct, fk_list in generics.items():
            ct_model = content_types[ct].model_class()
            relations[ct] = ct_model.objects.in_bulk(list(fk_list))

        for item in queryset:
            setattr(item, '_content_object_cache', 
                    relations[item.content_type_id][item.object_id])
        
        return queryset
        


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
    user = models.ForeignKey(User,
                             blank=False,
                             verbose_name=_(u"Usuario")
                             )
    msg_id = models.PositiveSmallIntegerField(_(u"Tipo de mensaje"))
    content_type = models.ForeignKey(ContentType,
                                     verbose_name = _(u"Tipo de instancia"))
    object_id = models.PositiveIntegerField(_(u"Identificador de instancia"))
    instance = generic.GenericForeignKey('content_type', 'object_id') # clave generica para cualquier modelo    
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
        ordering = ['-created']
        verbose_name = _(u"Timeline")
        verbose_name_plural = _(u"Timelines")
        
    def __unicode__(self):
        return "%s - %d - %s" % (self.user, self.id, self.modified)
    
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
            raise
            transaction.rollback()
        else:
            transaction.commit()
        

class TimelineFollower(models.Model):
    timeline = models.ForeignKey(Timeline,
                                 blank=False)
    
    follower_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _(u"Tipo de objeto seguidor"),
                                        related_name = "timelinefollowings")
    follower_id = models.PositiveIntegerField(_(u"Identificador del seguidor"))
    follower = generic.GenericForeignKey('follower_c_type', 'follower_id',) # clave generica para cualquier modelo
    
    created = LocalizedDateTimeField(auto_now_add=True)
    objects = TimelineFollowerManager()
    
    class Meta:
        get_latest_by = "created"
        ordering = ['-created']
        unique_together = (("timeline", "follower_c_type", "follower_id"),)
        verbose_name = _(u"Seguidor de Timeline")
        verbose_name_plural = _(u"Seguidores de Timelines")
        
    def __unicode__(self):
        return "%s - %d - %s" % (self.follower, self.timeline_id, self.created)
    


class TimelineNotificationManager(models.Manager):
    def add_notification(self, timeline, user=None):
        if user is None:
            obj = self.create(timeline = timeline,
                              user = timeline.user
                              )
        else:
            obj = self.create(timeline = timeline,
                              user = user
                              )
        notification_added.send(sender=obj)
        UserProfile.objects.filter(
                                   user = user
                                   ).update(
                                            counter_notifications = F('counter_notifications') + 1
                                            )
        return obj

    def get_by_user(self, user):
        user_type = ContentType.objects.get_for_model(user)
        return Timeline.objects.filter(
                                       timelinenotification__user_c_type = user_type,
                                       timelinenotification__user_id = user.id,
                                       ).select_related(depth=1)


class TimelineNotification(models.Model):
    timeline = models.ForeignKey(Timeline,
                                 blank=False)
    
    user_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _(u"Tipo de objeto seguidor"),
                                        related_name = "timelinenotifications")
    user_id = models.PositiveIntegerField(_(u"Identificador del seguidor"))
    user = generic.GenericForeignKey('user_c_type', 'user_id',) # clave generica para cualquier modelo
    created = LocalizedDateTimeField(auto_now_add=True)
    
    objects = TimelineNotificationManager()
    
    class Meta:
        get_latest_by = "created"
        ordering = ['-created']
        verbose_name = _(u"Notificacion de Timeline")
        verbose_name_plural = _(u"Notificaciones de Timelines")
        
    def __unicode__(self):
        return "%s - %d - %s" % (self.user, self.timeline_id, self.created)
    

from profiles.models import UserProfile