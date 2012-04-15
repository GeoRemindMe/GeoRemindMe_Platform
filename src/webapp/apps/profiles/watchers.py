#coding=utf-8

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from timelines.models import Timeline
from models import UserProfile
from funcs import DEBUG


@receiver(post_save, sender=User)
def new_user_registered(sender, instance, created, **kwargs):
    """
    Captura la señal de un nuevo usuario registrado,
    escribe el primer timeline
    """
    if instance.id <> -1 and created:
        try:
            instance.get_profile()
        except:
            UserProfile.objects.create(user=instance)
            
        Timeline.objects.add_timeline(actor=instance, 
                                      msg_id=0,
                                      objetive=instance,
                                      visible=False,
                                      )
        DEBUG('TIMELINE: creado nuevo usuario %s' % instance)