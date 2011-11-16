#coding=utf-8

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.utils import simplejson
from django.http import Http404

from socialregistration.signals import connect

from client import Twitter


class TwitterProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    twitter_id = models.PositiveIntegerField()

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.twitter_id)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(twitter_id=self.twitter_id)
    
    def _get_client(self):
        try:
            accessToken = self.access_token
        except TwitterRequestToken.DoesNotExist:
            raise Http404
        return Twitter(access_token=accessToken.oauth_token,
                         access_token_secret=accessToken.oauth_token_secret
                         )
    
    def get_avatar_url(self, secure=True):
        client = self._get_client()
        info = simplejson.loads(client.get_user_info())
        return info['profile_image_url']
    
    def send_tweet(self, msg, poi, wrap_links=False):
        client = self._get_client()
        return simplejson.loads(client.tweet(msg=msg, poi=poi, wrap_links=wrap_links))
        

class TwitterRequestToken(models.Model):
    profile = models.OneToOneField(TwitterProfile, related_name='request_token')
    oauth_token = models.CharField(max_length=80)
    oauth_token_secret = models.CharField(max_length=80)


class TwitterAccessToken(models.Model):
    profile = models.OneToOneField(TwitterProfile, related_name='access_token')
    oauth_token = models.CharField(max_length=80)
    oauth_token_secret = models.CharField(max_length=80)

    
def save_twitter_token(sender, user, profile, client, **kwargs):
    try:
        TwitterRequestToken.objects.get(profile=profile).delete()
    except TwitterRequestToken.DoesNotExist:
        pass
    try:
        TwitterAccessToken.objects.get(profile=profile).delete()
    except TwitterAccessToken.DoesNotExist:
        pass
    
    TwitterRequestToken.objects.create(profile=profile,
        oauth_token=client.get_request_token().key,
        oauth_token_secret=client.get_request_token().secret)
    
    TwitterAccessToken.objects.create(profile=profile,
        oauth_token=client.get_access_token().key,
        oauth_token_secret=client.get_access_token().secret)
    
connect.connect(save_twitter_token, sender=TwitterProfile,
    dispatch_uid='socialregistration_twitter_token')
