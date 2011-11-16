#coding=utf-8

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from socialregistration.clients.oauth import OAuth
import urlparse

class Twitter(OAuth):
    api_key = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
    secret_key = getattr(settings, 'TWITTER_CONSUMER_SECRET_KEY', '')
    
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    auth_url = 'https://api.twitter.com/oauth/authenticate'
    
    def get_callback_url(self):
        if self.is_https():
            return urlparse.urljoin(
                'https://%s' % Site.objects.get_current().domain,
                reverse('socialregistration:twitter:callback'))
        return urlparse.urljoin(
            'http://%s' % Site.objects.get_current().domain,
            reverse('socialregistration:twitter:callback'))
    
    @staticmethod
    def get_session_key():
        return 'socialreg:twitter'

    def get_user_info(self):
        if self._access_token_dict is not None:
            return self._access_token_dict
        else:
            return self._do_request(url='http://api.twitter.com/1/users/show.json/')
        
    def tweet(self, msg, poi=None, wrap_links=False):
        body = {
                'status': msg.encode('utf-8'),
                }
        if poi is not None:
            body['lat'] = poi.location.y
            body['lon'] = poi.location.x
        body['wrap_links'] = 'true' if wrap_links else 'false'
        
        from urllib import urlencode
        return self._do_request('https://api.twitter.com/1/statuses/update.json/', method='POST', body=urlencode(body))

    def _do_request(self, url, **kwargs):
        content = self.request(url, **kwargs)
        return content

