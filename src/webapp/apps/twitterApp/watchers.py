#coding=utf-8

import logging
logger = logging.getLogger(__name__)

from django.dispatch import receiver

from funcs import DEBUG
from events.signals import suggestion_new

@receiver(suggestion_new)
def new_suggestion(sender,  to_facebook=True, to_twitter=True, **kwargs):
    if to_twitter and sender._is_public():
            msg = "%(name)s %(url)s #grm" % {
                                            'name': sender.name[:100] + '...',
                                            'url': sender.short_url
                                            }
            try:
                twitterprofile = sender.user.twitterprofile
                DEBUG("TWITTER: Enviado tweet sugerencia: %s" % sender)
            except:
                return
            twitterprofile.send_tweet(msg, sender.poi.location)