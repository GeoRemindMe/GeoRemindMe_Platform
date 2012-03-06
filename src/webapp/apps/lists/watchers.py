#coding=utf-8

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.db import transaction


from timelines.models import Timeline, TimelineNotification
from models import ListFollower
from profiles.models import UserProfile
from signals import * #@UnusedWildImport
from funcs import DEBUG


@transaction.commit_on_success()
@receiver(list_new)
def new_list(sender, instance, created, **kwargs):
    """
    Captura la señal de un nuevo usuario registrado,
    escribe el primer timeline
    """
    f = ListFollower.objects.create(list_instance=instance, user=instance.user)
    Timeline.objects.add_timeline(actor = instance.user,
                                  msg_id = 350,
                                  instance = instance,
                                  result = f,
                                  visible = True if sender._is_public() else False)
    #UserProfile.objects.set_suggested(sender.user, value=1)
    DEBUG('TIMELINE: creada nueva lista %s' % sender)


@transaction.commit_on_success()
@receiver(post_save, sender = ListFollower)
def added_list_following(sender, instance, created, **kwargs):
    if created and instance.user_id != instance.event.user_id:
        t = Timeline.objects.add_timeline(actor = instance.user,
                                      msg_id = 353,
                                      objetive = instance.list_instance,
                                      result = instance,
                                      visible = True if sender._is_public() else False)
        #UserProfile.objects.set_supported(follower)
        instance.list_instance.__class___.objects.set_followers(instance.list_instance)
        TimelineNotification.objects.add_notification(timeline=t)
        DEBUG('TIMELINE: usuario %s sigue lista %s' % (instance.user, instance.list_instance))
    
    
#@receiver(list_following_deleted)
#def deleted_suggestion_following(sender, follower, **kwargs):
#    list_type = ContentType.objects.get_for_model(sender)
#    ListFollower.objects.filter(user = follower, 
#                                 list_c_type = list_type,
#                                 list_id = sender.id).delete()
#    ListSuggestion.objects.set_followers(sender, value=-1)
#    #UserProfile.objects.set_supported(follower, value=-1)
#    DEBUG('TIMELINE: usuario %s deja de seguir lista %s' % (follower, sender))