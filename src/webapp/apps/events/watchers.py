#coding=utf-8

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.contrib.contenttypes.models import ContentType


from timelines.models import Timeline, TimelineNotification
from models import Suggestion, EventFollower
from profiles.models import UserProfile
from signals import * #@UnusedWildImport
from funcs import DEBUG


@receiver(post_save, sender=Suggestion)
def new_suggestion(sender, instance, created, **kwargs):
    """
    Captura la señal de un nuevo usuario registrado,
    escribe el primer timeline
    """
    if created:
        EventFollower.objects.create(event=instance, user=instance.user)
        Timeline.objects.add_timeline(user = instance.user,
                                      msg_id = 300,
                                      instance = instance,
                                      visible = True if instance._is_public() else False)
        DEBUG('TIMELINE: creada nueva sugerencia %s' % instance)
        
        
@receiver(pre_delete, sender=Suggestion)
def deleted_suggestion(sender, instance, **kwargs):
    UserProfile.objects.set_suggested(instance.user, value=-1)
        
        
@receiver(post_save, sender=EventFollower)
def added_suggestion_following(sender, instance, **kwargs):
    t = Timeline.objects.add_timeline(user = instance.user,
                                  msg_id = 303,
                                  objetive = instance,
                                  visible = True if sender._is_public() else False)
    UserProfile.objects.set_supported(instance.user)
    instance.__class__.objects.set_followers(instance.event)
    TimelineNotification.objects.add_notification(timeline=t)
    DEBUG('TIMELINE: usuario %s sigue evento %s' % (instance.user, instance))
    
    
@receiver(pre_delete, sender=EventFollower)
def deleted_suggestion_following(sender, instance, **kwargs):
    UserProfile.objects.set_supported(instance.user, value=-1)
    instance.__class__.objects.set_followers(instance.event, value=-1)
    DEBUG('TIMELINE: usuario %s deja de seguir evento %s' % (instance.user, instance))