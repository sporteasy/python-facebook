import time
import urllib

from python_facebook.sdk.authentication.access_token import AccessToken
from python_facebook.sdk.authentication.access_token_metadata import AccessTokenMetadata
from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException
from python_facebook.sdk.facebook import Facebook
from python_facebook.sdk.request import FacebookRequest


class Oauth2Client(object):
    BASE_AUTHORIZATION_URL = 'https://www.facebook.com'

    def __init__(self, app, client, graph_version=None):
        self.app = app
        self.client = client
        self.graph_version = graph_version or Facebook.DEFAULT_GRAPH_VERSION

        self.last_request = None

    def get_last_request(self):
        return self.last_request

    def debug_token(self, access_token):
        access_token = access_token.get_value() if isinstance(access_token, AccessToken) else access_token
        params = {
            'input_token': access_token
        }

        self.last_request = FacebookRequest(
            self.app,
            self.app.get_access_token(),
            'GET',
            '/debug_token',
            params,
            None,
            self.graph_version
        )
        response = self.client.send_request(self.last_request)
        metadata = response.get_decoded_body()

        return AccessTokenMetadata(metadata)

    def get_authorization_url(self, redirect_url, state, scope=None, params=None, separator='&'):
        """
        Generates an authorization URL to begin the process of authenticating a user.
        """
        if not params:
            params = {}

        if not scope:
            scope = []

        params.update({
            'client_id': self.app.get_id(),
            'state': state,
            'response_type': 'code',
            'sdk': 'python-sdk-' + Facebook.VERSION,
            'redirect_uri': redirect_url,
            'scope': ','.join(scope)
        })

        return self.BASE_AUTHORIZATION_URL + '/' + self.graph_version + 'dialog/oauth?' + \
            urllib.urlencode(sorted(params.items()))

    def get_access_token_from_code(self, code, redirect_uri=''):
        """
        Get a valid access token from a code.
        """
        params = {
            'code': code,
            'redirect_uri': redirect_uri
        }
        return self.request_an_access_token(params)

    def get_long_lived_access_token(self, access_token):
        """
        Exchanges a short-lived access token with a long-lived access token.
        """
        access_token = access_token.get_value() if isinstance(access_token, AccessToken) else access_token
        params = {
            'grant_type': 'fb_exchange_token',
            'fb_exchange_token': access_token
        }
        return self.request_an_access_token(params)

    def get_code_from_long_lived_access_token(self, access_token, redirect_uri=''):
        """
        Get a valid code from an access token
        """
        params = {
            'redirect_uri': redirect_uri
        }
        response = self.send_request_with_client_params('/oauth/client_code', params, access_token)
        data = response.get_decoded_body()

        if not data.get('code'):
            raise FacebookSDKException('Code was not returned from Graph.', 401)

        return data['code']

    def request_an_access_token(self, params):
        """
        Send a request to the OAuth endpoint.
        """
        response = self.send_request_with_client_params('/oauth/access_token', params)
        data = response.get_decoded_body()

        if not data.get('access_token'):
            raise FacebookSDKException('Access token was not returned from Graph.', 401)

        # Graph returns two different key names for expiration time
        # on the same endpoint. Doh! :/
        expires_at = 0
        if data.get('expires'):
            # For exchanging a short lived token with a long lived token.
            # The expiration time in seconds will be returned as "expires".
            expires_at = time.time() + data['expires']
        elif data.get('expires_in'):
            # For exchanging a code for a short lived access token.
            # The expiration time in seconds will be returned as "expires_in".
            # See: https://developers.facebook.com/docs/facebook-login/access-tokens#long-via-code
            expires_at = time.time() + data['expires_in']

        return AccessToken(data['access_token'], expires_at)

    def send_request_with_client_params(self, endpoint, params, access_token=None):
        """
        Send a request to Graph with an app access token.
        """
        params.update(self.get_client_params())

        access_token = access_token or self.app.get_access_token()

        self.last_request = FacebookRequest(
            self.app,
            access_token,
            'GET',
            endpoint,
            params,
            None,
            self.graph_version
        )

        return self.client.send_request(self.last_request)

    def get_client_params(self):
        """
        Returns the client_* params for OAuth requests.
        """
        return {
            'client_id': self.app.get_id(),
            'client_secret': self.app.get_secret()
        }
