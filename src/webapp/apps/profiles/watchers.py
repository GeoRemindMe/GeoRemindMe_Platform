#coding=utf-8

import logging
logger = logging.getLogger(__name__)

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from timelines.models import Timeline
from webapp.site.funcs import DEBUG


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