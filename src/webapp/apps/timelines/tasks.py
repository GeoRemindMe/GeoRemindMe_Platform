# codign=utf-8

from django.dispatch import receiver
from django.contrib.auth.models import User

from celery.decorators import task

from signals import timeline_added
import models as timelines_models


@receiver(timeline_added, dispatch_uid="timeline_sharing")
@task()
def share_timeline(sender, **kwargs):
    timeline = sender
    if timeline.visible:
        followers = timelines_models.Follower.objects.get_by_followee(followee = timeline.user,
                                                                      type_filter = User)
        timelines = []
        for follower in (follower.follower for follower in followers):
            timelines.append(timelines_models.TimelineFollower(timeline = timeline,
                                                              follower = follower))
        timelines_models.TimelineFollower.objects.bulk_create(timelines)
