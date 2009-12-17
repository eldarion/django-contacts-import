import httplib2
import socket

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import simplejson as json

import oauth2 as oauth


class ServiceFail(Exception):
    pass


class oAuthConsumer(object):
    
    def __init__(self, service):
        self.service = service
        self.signature_method = oauth.SignatureMethod_HMAC_SHA1()
        self.consumer = oauth.Consumer(self.key, self.secret)
    
    @property
    def key(self):
        return self._obtain_setting("keys", "KEY")
    
    @property
    def secret(self):
        return self._obtain_setting("keys", "SECRET")
    
    @property
    def request_token_url(self):
        return self._obtain_setting("endpoints", "request_token")
    
    @property
    def access_token_url(self):
        return self._obtain_setting("endpoints", "access_token")
    
    @property
    def authorize_url(self):
        return self._obtain_setting("endpoints", "authorize")
    
    def _obtain_setting(self, k1, k2):
        name = "OAUTH_CONSUMER_SETTINGS"
        service = self.service
        try:
            return getattr(settings, name)[service][k1][k2]
        except AttributeError:
            raise ImproperlyConfigured("%s must be defined in settings" % (name,))
        except KeyError, e:
            key = e.args[0]
            if key == service:
                raise ImproperlyConfigured("%s must contain '%s'" % (name, service))
            elif key == k1:
                raise ImproperlyConfigured("%s must contain '%s' for '%s'" % (name, k1, service))
            elif key == k2:
                raise ImproperlyConfigured("%s must contain '%s' for '%s' in '%s'" % (name, k2, k1, service))
            else:
                raise
    
    def unauthorized_token(self):
        if not hasattr(self, "_unauthorized_token"):
            self._unauthorized_token = self.fetch_unauthorized_token()
        return self._unauthorized_token
    
    def fetch_unauthorized_token(self):
        request = oauth.Request.from_consumer_and_token(self.consumer,
            http_url = self.request_token_url,
            parameters = {
                # @@@ fixme
                "oauth_callback": "http://contacts-import.pinaxproject.com/c/import_contacts/",
            }
        )
        request.sign_request(self.signature_method, self.consumer, None)
        try:
            return oauth.Token.from_string(self._oauth_response(request))
        except KeyError, e:
            if e.args[0] == "oauth_token":
                raise ServiceFail()
            raise
    
    def authorized_token(self, token):
        request = oauth.Request.from_consumer_and_token(self.consumer,
            token = token,
            http_url = self.access_token_url,
        )
        request.sign_request(self.signature_method, self.consumer, token)
        try:
            return oauth.Token.from_string(self._oauth_response(request))
        except KeyError:
            raise ServiceFail()
    
    def authorization_url(self, token):
        request = oauth.Request.from_consumer_and_token(
            self.consumer,
            token = token,
            http_url = self.authorize_url,
        )
        request.sign_request(self.signature_method, self.consumer, token)
        return request.to_url()
    
    def make_api_call(self, url, token, http_method="GET", **kwargs):
        response = self._oauth_response(
            self._oauth_request(url, token,
                http_method = http_method,
                params = kwargs,
            )
        )
        if not response:
            raise ServiceFail()
        try:
            return json.loads(response)
        except ValueError:
            raise ServiceFail()
    
    def _oauth_request(self, url, token, http_method="GET", params=None):
        request = oauth.Request.from_consumer_and_token(self.consumer,
            token = token,
            http_url = url,
            parameters = params,
            http_method = http_method,
        )
        request.sign_request(self.signature_method, self.consumer, token)
        return request
    
    def _oauth_response(self, request):
        http = httplib2.Http()
        # @@@ hack for now
        if request.http_method == "POST":
            ret = http.request(request.http_url, "POST", request.to_postdata())
        else:
            ret = http.request(request.to_url(), "GET")
        response, content = ret
        return content
