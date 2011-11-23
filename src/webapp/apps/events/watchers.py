#coding=utf-8

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType


from timelines.models import Timeline
from models import Suggestion, EventFollower
from signals import * #@UnusedWildImport
from webapp.site.funcs import DEBUG


@receiver(post_save, sender=Suggestion)
def new_suggestion(sender, instance, created, **kwargs):
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
        
        
@receiver(suggestion_following_added)
def added_suggestion_following(sender, follower, **kwargs):
    Timeline.objects.add_timeline(user = follower,
                                  msg_id = 303,
                                  instance = sender,
                                  visible = True if sender._is_public() else False)
    DEBUG('TIMELINE: usuario %s sigue sugerencia %s' % (follower, sender))
    
    
@receiver(suggestion_following_deleted)
def deleted_suggestion_following(sender, follower, **kwargs):
    suggestion_type = ContentType.objects.get_for_model(sender)
    EventFollower.objects.filter(user = follower, 
                                 event_c_type = suggestion_type,
                                 event_id = sender.id).delete()
    DEBUG('TIMELINE: usuario %s deja de seguir sugerencia %s' % (follower, sender))