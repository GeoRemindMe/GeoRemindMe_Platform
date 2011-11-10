# coding=utf-8

import logging
logger = logging.getLogger(__name__)

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from models import Timeline, NotificationSettings
from funcs import DEBUG
from signals import follower_added, follower_deleted


@receiver(post_save, sender=User)
def new_user_registered(sender, instance, created, **kwargs):
    """
    Captura la señal de un nuevo usuario registrado,
    escribe el primer timeline
    """
    if instance.id <> -1 and created:
        Timeline.objects.add_timeline(user = instance,
                                          msg_id = 0,
                                          instance = instance,
                                          visible = False)
        DEBUG('TIMELINE: creado nuevo usuario %s' % instance)
        

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
    Timeline.objects.add_timeline(sender, 
                                  msg_id=100,
                                  instance=followee,
                                  visible=True)
    DEBUG('TIMELINE: %s ahora sigue a %s' % (sender, followee))
          

@receiver(follower_deleted)
def deleted_follower(sender, followee, **kwargs):
    Timeline.objects.del_all_timelines(user = sender,
                                       msg_id = 100,
                                       instance = followee)
    DEBUG('TIMELINE: %s ya no sigue a %s' % (sender, followee))
