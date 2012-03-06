#coding=utf-8

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, pre_save
from django.db import transaction
from django.contrib.contenttypes.models import ContentType


from timelines.models import Timeline, TimelineNotification
from models import Suggestion, EventFollower
from profiles.models import UserProfile
from signals import * #@UnusedWildImport
from funcs import DEBUG

@transaction.commit_on_success()
@receiver(suggestion_new, sender=Suggestion)
def new_suggestion(sender, instance, created, **kwargs):
    """
    Captura la señal de un nuevo usuario registrado,
    escribe el primer timeline
    """
    if created:
        f = EventFollower.objects.create(event=instance, user=instance.user)
        Timeline.objects.add_timeline(actor = instance.user,
                                      msg_id = 300,
                                      objetive = instance,
                                      result = f,
                                      visible = True if instance._is_public() else False)
        UserProfile.objects.set_suggested(instance.user)
        DEBUG('TIMELINE: creada nueva sugerencia %s' % instance)
        
        
@receiver(pre_delete, sender=Suggestion)
def deleted_suggestion(sender, instance, **kwargs):
    UserProfile.objects.set_suggested(instance.user, value=-1)
        

@transaction.commit_on_success()        
@receiver(post_save, sender=EventFollower)
def added_suggestion_following(sender, instance, created, **kwargs):
    if created and instance.user_id != instance.event.user_id:
        t = Timeline.objects.add_timeline(actor = instance.user,
                                      msg_id = 303,
                                      objetive = instance.event,
                                      result = instance,
                                      visible = True if instance.event._is_public() else False)
        TimelineNotification.objects.add_notification(timeline=t)
        UserProfile.objects.set_supported(instance.user)
        instance.event.__class__.objects.set_followers(instance.event)
    
    DEBUG('TIMELINE: usuario %s sigue evento %s' % (instance.user, instance))
    
    
@transaction.commit_on_success()
@receiver(pre_delete, sender=EventFollower)
def deleted_suggestion_following(sender, instance, **kwargs):
    UserProfile.objects.set_supported(instance.user, value=-1)
    instance.event.__class__.objects.set_followers(instance.event, value=-1)
    DEBUG('TIMELINE: usuario %s deja de seguir evento %s' % (instance.user, instance))
    
    
@receiver(pre_save, sender=Suggestion)
def suggestion_modified(sender, instance, raw, **kwargs):
    if not raw and instance.place is not None:
        instance.location = instance.place.location