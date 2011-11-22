#coding=utf-8

from django.dispatch import receiver
from django.db.models.signals import post_save

from timelines.models import Timeline
from models import Suggestion
from webapp.site.funcs import DEBUG


@receiver(post_save, sender=Suggestion)
def new_user_registered(sender, instance, created, **kwargs):
    """
    Captura la señal de un nuevo usuario registrado,
    escribe el primer timeline
    """
    if created:
        Timeline.objects.add_timeline(user = instance.user,
                                      msg_id = 300,
                                      instance = instance,
                                      visible = True if instance._is_public() else False)
        DEBUG('TIMELINE: creada nueva sugerencia %s' % instance)