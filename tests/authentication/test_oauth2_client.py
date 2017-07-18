import unittest
import urllib

from python_facebook.sdk.authentication.access_token import AccessToken
from python_facebook.sdk.authentication.access_token_metadata import AccessTokenMetadata
from python_facebook.sdk.authentication.oauth2_client import OAuth2Client
from python_facebook.sdk.facebook import Facebook
from python_facebook.sdk.facebook_app import FacebookApp
from tests.authentication.foo_facebook_client_for_oauth2_test import FooFacebookClientForOAuth2Test


class OAuth2ClientTestCase(unittest.TestCase):
    TESTING_GRAPH_VERSION = 'v1337'

    def setUp(self):
        app = FacebookApp('123', 'foo_secret')
        self.client = FooFacebookClientForOAuth2Test()
        self.oauth = OAuth2Client(app, self.client, self.TESTING_GRAPH_VERSION)

    def test_can_get_metadata_from_an_access_token(self):

        self.client.set_metadata_response()

        metadata = self.oauth.debug_token('baz_token')

        self.assertIsInstance(metadata, AccessTokenMetadata)
        self.assertEqual('444', metadata.get_user_id())

        expected_params = {
            'input_token': 'baz_token',
            'access_token': '123|foo_secret',
            'appsecret_proof': 'de753c58fd58b03afca2340bbaeb4ecf987b5de4c09e39a63c944dd25efbc234'
        }

        request = self.oauth.get_last_request()
        self.assertEqual('GET', request.get_method())
        self.assertEqual('/debug_token', request.get_endpoint())
        self.assertEqual(expected_params, request.get_params())
        self.assertEqual(self.TESTING_GRAPH_VERSION, request.get_graph_version())

    def test_can_build_authorization_url(self):
        scope = ['email', 'base_foo']
        oauth_url = self.oauth.get_authorization_url(
            'https://foo.bar',
            'foo_state',
            scope,
            {'foo': 'bar'}
        )

        expected_url = 'https://www.facebook.com/' + self.TESTING_GRAPH_VERSION + '/dialog/oauth?'
        self.assertTrue(oauth_url.startswith(expected_url),
                        'Unexpected base authorization URL returned from getAuthorizationUrl().')

        params = {
            'client_id': '123',
            'redirect_uri': 'https://foo.bar',
            'state': 'foo_state',
            'sdk': 'python-sdk-' + Facebook.VERSION,
            'scope': ','.join(scope),
            'foo': 'bar'
        }
        for key, value in params.items():
            self.assertIn('{}={}'.format(key, urllib.quote_plus(value)), oauth_url,
                          '{}={} not found in oauth_url'.format(key, urllib.quote_plus(value)))

    def test_can_get_access_token_from_code(self):
        self.client.set_access_token_response()

        access_token = self.oauth.get_access_token_from_code('bar_code', 'foo_uri')

        self.assertIsInstance(access_token, AccessToken)
        self.assertEqual('my_access_token', access_token.get_value())

        expected_params = {
            'code': 'bar_code',
            'redirect_uri': 'foo_uri',
            'client_id': '123',
            'client_secret': 'foo_secret',
            'access_token': '123|foo_secret',
            'appsecret_proof': 'de753c58fd58b03afca2340bbaeb4ecf987b5de4c09e39a63c944dd25efbc234'
        }

        request = self.oauth.get_last_request()
        self.assertEqual('GET', request.get_method())
        self.assertEqual('/oauth/access_token', request.get_endpoint())
        self.assertEqual(expected_params, request.get_params())
        self.assertEqual(self.TESTING_GRAPH_VERSION, request.get_graph_version())

    def test_can_get_long_lived_access_token(self):
        self.client.set_access_token_response()

        access_token = self.oauth.get_long_lived_access_token('short_token')

        self.assertEqual('my_access_token', access_token.get_value())

        expected_params = {
            'grant_type': 'fb_exchange_token',
            'fb_exchange_token': 'short_token',
            'client_id': '123',
            'client_secret': 'foo_secret',
            'access_token': '123|foo_secret',
            'appsecret_proof': 'de753c58fd58b03afca2340bbaeb4ecf987b5de4c09e39a63c944dd25efbc234'
        }

        request = self.oauth.get_last_request()
        self.assertEqual(expected_params, request.get_params())

    def test_can_get_code_from_long_lived_access_token(self):
        self.client.set_code_response()

        code = self.oauth.get_code_from_long_lived_access_token('long_token', 'foo_uri')

        self.assertEqual('my_neat_code', code)

        expected_params = {
            'access_token': 'long_token',
            'redirect_uri': 'foo_uri',
            'client_id': '123',
            'client_secret': 'foo_secret',
            'appsecret_proof': '7e91300ea91be4166282611d4fc700b473466f3ea2981dafbf492fc096995bf1'
        }

        request = self.oauth.get_last_request()

        self.assertEqual(expected_params, request.get_params())
        self.assertEqual('/oauth/client_code', request.get_endpoint())
