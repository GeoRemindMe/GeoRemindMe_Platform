#coding=utf-8

from django.conf import settings
from django.db.models import signals
from django.contrib.auth.models import User

from guardian import models as guardian_app



def create_georemindme_user(sender, **kwargs):
    """
    Creates anonymous User instance with id from settings.
    """
    try:
        User.objects.get(pk=settings.GEOREMINDME_USER_ID)
    except User.DoesNotExist:
        User.objects.create(pk=settings.GEOREMINDME_USER_ID,
            username='georemindme')

signals.post_syncdb.connect(create_georemindme_user, sender=guardian_app,
    dispatch_uid="mainApp.management.create_georemindme_user")