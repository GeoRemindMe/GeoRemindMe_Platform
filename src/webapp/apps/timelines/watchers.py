#coding=utf-8

import logging
logger = logging.getLogger(__name__)

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from models import Timeline, NotificationSettings, TimelineNotification, Follower
from profiles.models import UserProfile
from funcs import DEBUG
        

@receiver(post_save, sender=User)
def create_notificationssettings(sender, instance, created, **kwargs):
    """
    Captura la señal de un nuevo usuario registrado,
    le crea la configuracion de notificaciones
    """
    if instance.id <> -1 and created:
        NotificationSettings.objects.create(user = instance)


@receiver(post_save, sender=Follower)
def new_follower(sender,  instance, created, **kwargs):
    if created:
        t = Timeline.objects.add_timeline(actor=instance.follower, 
                                      msg_id=100,
                                      objetive=instance.followee,
                                      visible=True)
        UserProfile.objects.set_followers(user=instance.followee) # incrementa el contador del followee
        UserProfile.objects.set_followings(user=instance.follower) # incrementa el contador del follower
        TimelineNotification.objects.add_notification(timeline=t, user = instance.followee)
        
        DEBUG('TIMELINE: %s ahora sigue a %s' % (instance.follower, instance.followee))
          

@receiver(pre_delete, sender=Follower)
def deleted_follower(sender, instance, **kwargs):
    UserProfile.objects.set_followers(user=instance.followee, value=-1)
    UserProfile.objects.set_followings(user=instance.follower, value=-1)
    
    DEBUG('TIMELINE: %s ya no sigue a %s' % (instance.follower, instance.followee))


#@receiver(pre_delete)
#def deleted_object_in_timeline(sender, instance, **kwargs):
#    instance_ct = ContentType.objects.get_for_model(instance)
#    if type(instance.pk) is int:
#        Timeline.objects.filter(Q(objetive_c_type=instance_ct, objetive_id=instance.pk) 
#                            | Q(result_c_type=instance_ct, result_id=instance.pk)
#                            ).delete()
#        UserProfile.objects.set_followers(user=instance.followee, value=-1)
#        UserProfile.objects.set_followings(user=instance.follower, value=-1)
#    
#        DEBUG('TIMELINE: %s ya no sigue a %s' % (instance.follower, instance.followee))
    

