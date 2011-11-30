#coding=utf-8

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType


from timelines.models import Timeline, TimelineNotification
from models import ListSuggestion, ListFollower
from profiles.models import UserProfile
from signals import * #@UnusedWildImport
from funcs import DEBUG


@receiver(list_new)
def new_list(sender, **kwargs):
    """
    Captura la señal de un nuevo usuario registrado,
    escribe el primer timeline
    """
    ListFollower.objects.create(list_instance=sender, user=sender.user)
    Timeline.objects.add_timeline(user = sender.user,
                                  msg_id = 350,
                                  instance = sender,
                                  visible = True if sender._is_public() else False)
    #UserProfile.objects.set_suggested(sender.user, value=1)
    DEBUG('TIMELINE: creada nueva lista %s' % sender)
        
        
#@receiver(list_deleted)
#def deleted_suggestion(sender, **kwargs):
#    UserProfile.objects.set_suggested(sender.user, value=-1)
        
        
@receiver(list_following_added)
def added_list_following(sender, follower, **kwargs):
    t = Timeline.objects.add_timeline(user = follower,
                                  msg_id = 353,
                                  instance = sender,
                                  visible = True if sender._is_public() else False)
    #UserProfile.objects.set_supported(follower)
    ListSuggestion.objects.set_followers(sender)
    TimelineNotification.objects.add_notification(timeline=t)
    
    DEBUG('TIMELINE: usuario %s sigue lista %s' % (follower, sender))
    
    
@receiver(list_following_deleted)
def deleted_suggestion_following(sender, follower, **kwargs):
    list_type = ContentType.objects.get_for_model(sender)
    ListFollower.objects.filter(user = follower, 
                                 list_c_type = list_type,
                                 list_id = sender.id).delete()
    ListSuggestion.objects.set_followers(sender, value=-1)
    #UserProfile.objects.set_supported(follower, value=-1)
    DEBUG('TIMELINE: usuario %s deja de seguir lista %s' % (follower, sender))