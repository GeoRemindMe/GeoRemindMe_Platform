# coding=utf-8

import watchers

from django.contrib import auth


def natural_key(self):
    return (self.pk, self.username)

auth.models.User.add_to_class('natural_key', natural_key)

def is_follower(self, followee):
    return Follower.objects.is_follower(follower=self,
                                        followee = followee)
    
auth.models.User.add_to_class('is_follower', is_follower)
    
def toggle_follower(self, followee):
    return Follower.objects.toggle_follower(follower=self,
                                            followee = followee)
    
auth.models.User.add_to_class('toggle_follower', toggle_follower)


def get_chronology(self):
    return Timeline.objects.get_chronology(self)

auth.models.User.add_to_class('get_chronology', get_chronology)

def get_notifications(self):
    return TimelineNotification.objects.get_by_user(self) 

auth.models.User.add_to_class('get_notifications', get_notifications)

from timelines.models import Timeline, Follower, TimelineNotification