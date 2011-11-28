#coding=utf-8

import logging
logger = logging.getLogger(__name__)

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from models import Timeline, NotificationSettings, TimelineNotification
from profiles.models import UserProfile
from funcs import DEBUG
from signals import follower_added, follower_deleted
        

@receiver(post_save, sender=User)
def create_notificationssettings(sender, instance, created, **kwargs):
    """
    Captura la señal de un nuevo usuario registrado,
    le crea la configuracion de notificaciones
    """
    if instance.id <> -1 and created:
        NotificationSettings.objects.create(user = instance)


@receiver(follower_added)
def new_follower(sender,  followee, **kwargs):
    t = Timeline.objects.add_timeline(sender, 
                                  msg_id=100,
                                  instance=followee,
                                  visible=True)
    UserProfile.objects.set_followers(user=sender)
    UserProfile.objects.set_followings(user=followee)
    TimelineNotification.objects.add_notification(timeline=t)
    
    DEBUG('TIMELINE: %s ahora sigue a %s' % (sender, followee))
          

@receiver(follower_deleted)
def deleted_follower(sender, followee, **kwargs):
    UserProfile.objects.set_followers(user=sender, value=-1)
    UserProfile.objects.set_followings(user=followee, value=-1)
    
    DEBUG('TIMELINE: %s ya no sigue a %s' % (sender, followee))
