# codign=utf-8

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from celery.task import task

import models as timelines_models


#@task
def share_timeline(timeline):
    if timeline.visible:
        followers = timelines_models.Follower.objects.get_by_followee(followee = timeline.actor,
                                                                      type_filter = User
                                                                      )
        timelines = []
        for follower in followers:
            timelines.append(timelines_models.TimelineFollower(timeline = timeline,
                                                              follower = follower))
        timelines_models.TimelineFollower.objects.bulk_create(timelines)


@receiver(post_save, sender=timelines_models.Timeline, dispatch_uid="timeline_sharing")
def watcher_share_timeline(sender, instance, created, **kwargs):
    if created and instance.actor_id != -2:
        share_timeline.delay(instance)
