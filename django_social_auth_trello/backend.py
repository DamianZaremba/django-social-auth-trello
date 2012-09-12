'''
Django Social Auth - Trello
===========================
A [django-social-auth](https://github.com/omab/django-social-auth/) module that
authenticates against Trello.
'''
from django.utils import simplejson
from django.conf import settings

from oauth2 import Token
from urllib import urlencode
from urllib2 import urlopen

try:
    from urlparse import parse_qs
except ImportError:
    # The dark ages
    from cgi import parse_qs

from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, USERNAME
from social_auth.backends.exceptions import AuthCanceled

API_SERVER = 'trello.com'

class TrelloBackend(OAuthBackend):
    '''Trello authentication backend'''
    name = 'trello'

    def get_user_id(self, details, response):
        '''Return the user id'''
        return response['id']

    def get_user_details(self, response):
        '''Return user details'''
        try:
            first_name, last_name = response['fullName'].split(' ', 1)
        except ValueError:
            first_name = response['fullName']
            last_name = ''

        return {USERNAME: response['username'],
                'email': '',
                'fullname': ['fullName'],
                'first_name': first_name,
                'last_name': last_name}


class TrelloAuth(ConsumerBasedOAuth):
    """Trello OAuth authentication mechanism"""
    SERVER_URL = API_SERVER
    AUTHORIZATION_URL = 'https://%s/1/OAuthAuthorizeToken' % API_SERVER
    REQUEST_TOKEN_URL = 'https://%s/1/OAuthGetRequestToken' % API_SERVER
    ACCESS_TOKEN_URL = 'https://%s/1/OAuthGetAccessToken' % API_SERVER

    AUTH_BACKEND = TrelloBackend

    SETTINGS_KEY_NAME = 'TRELLO_API_KEY'
    SETTINGS_SECRET_NAME = 'TRELLO_API_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        '''Return user data from trello'''
        url = 'https://%s/1/members/me' % API_SERVER
        request = self.oauth_request(access_token, url)
        response = self.fetch_response(request)

        try:
            return simplejson.loads(response)
        except ValueError:
            return None

    def auth_extra_arguments(self):
        params = super(TrelloAuth, self).auth_extra_arguments() or {}
        if not 'scope' in params:
            params['scope'] = 'read,write'

        if not 'expires' in params:
            params['expires'] = 'never'
        return params

    @classmethod
    def api_key(cls):
        return getattr(settings, cls.SETTINGS_KEY_NAME, '')

# Backend definition
BACKENDS = {
    'trello': TrelloAuth,
}