import unittest
import urllib

from python_facebook.sdk.facebook import Facebook
from python_facebook.sdk.facebook_app import FacebookApp
from python_facebook.sdk.facebook_client import FacebookClient
from python_facebook.sdk.helpers.facebook_redirect_login_helper import FacebookRedirectLoginHelper
from python_facebook.sdk.persistent_data.facebook_memory_persistent_data_handler import \
    FacebookMemoryPersistentDataHandler
from tests.fixtures.foo_redirect_login_oauth2_client import FooRedirectLoginOAuth2Client


class FacebookRedirectLoginHelperTestCase(unittest.TestCase):
    REDIRECT_URL = 'http://invalid.zzz'

    def setUp(self):
        self.persistent_data_handler = FacebookMemoryPersistentDataHandler()

        app = FacebookApp('123', 'foo_app_secret')
        oauth2_client = FooRedirectLoginOAuth2Client(app, FacebookClient(), 'v1337')
        self.redirect_login_helper = FacebookRedirectLoginHelper(oauth2_client, self.persistent_data_handler)

    def test_login_url(self):
        scope = ['foo', 'bar']
        login_url = self.redirect_login_helper.get_login_url(self.REDIRECT_URL, scope)

        print login_url
        expected_url = 'https://www.facebook.com/v1337/dialog/oauth?'

        self.assertTrue(login_url.startswith(expected_url),
                        'Unexpected base login URL "{}" returned from get_login_url().'.format(login_url))

        params = {
            'client_id': '123',
            'redirect_uri': self.REDIRECT_URL,
            'state': self.persistent_data_handler.get('state'),
            'sdk': 'python-sdk-' + Facebook.VERSION,
            'scope': ','.join(scope)
        }

        for key, value in params.items():
            self.assertIn('{}={}'.format(key, urllib.quote_plus(value)), login_url,
                          '{}={} not found in login_url'.format(key, urllib.quote_plus(value)))

    def test_logout_url(self):
        logout_url = self.redirect_login_helper.get_logout_url('foo_token', self.REDIRECT_URL)
        expected_url = 'https://www.facebook.com/logout.php?'
        self.assertTrue(logout_url.startswith(expected_url),
                        'Unexpected base logout URL returned from get_logout_url().')

        params = {
            'next': self.REDIRECT_URL,
            'access_token': 'foo_token'
        }

        for key, value in params.items():
            self.assertIn('{}={}'.format(key, urllib.quote_plus(value)), logout_url,
                          '{}={} not found in logout_url'.format(key, urllib.quote_plus(value)))
