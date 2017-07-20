try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus
from tests import PythonFacebookTestCase
from python_facebook.sdk.facebook import Facebook
from python_facebook.sdk.facebook_app import FacebookApp
from python_facebook.sdk.facebook_client import FacebookClient
from python_facebook.sdk.helpers.facebook_redirect_login_helper import \
    FacebookRedirectLoginHelper
from python_facebook.sdk.persistent_data.\
    facebook_memory_persistent_data_handler import \
    FacebookMemoryPersistentDataHandler
from python_facebook.sdk.pseudo_random_string.\
    urandom_pseudo_random_string_generator import \
    UrandomPseudoRandomStringGenerator
from tests.fixtures.foo_pseudo_random_string_generator import \
    FooPseudoRandomStringGenerator
from tests.fixtures.foo_redirect_login_oauth2_client import \
    FooRedirectLoginOAuth2Client


class FacebookRedirectLoginHelperTestCase(PythonFacebookTestCase):
    REDIRECT_URL = 'http://invalid.zzz'

    def setUp(self):
        super(FacebookRedirectLoginHelperTestCase, self).setUp()
        self.persistent_data_handler = FacebookMemoryPersistentDataHandler()

        app = FacebookApp('123', 'foo_app_secret')
        oauth2_client = FooRedirectLoginOAuth2Client(app, FacebookClient(),
                                                     'v1337')
        self.redirect_login_helper = FacebookRedirectLoginHelper(
            oauth2_client, self.persistent_data_handler)

    def test_login_url(self):
        scope = ['foo', 'bar']
        login_url = self.redirect_login_helper.get_login_url(
            self.REDIRECT_URL, scope)

        expected_url = 'https://www.facebook.com/v1337/dialog/oauth?'

        self.assertTrue(
            login_url.startswith(expected_url),
            'Unexpected base login URL "{}" returned from '
            'get_login_url().'.format(login_url))

        params = {
            'client_id': '123',
            'redirect_uri': self.REDIRECT_URL,
            'state': self.persistent_data_handler.get('state'),
            'sdk': 'python-sdk-' + Facebook.VERSION,
            'scope': ','.join(scope)
        }

        for key, value in params.items():
            self.assertIn('{}={}'.format(key, quote_plus(value)),
                          login_url,
                          '{}={} not found in login_url'.format(
                              key, quote_plus(value)))

    def test_logout_url(self):
        logout_url = self.redirect_login_helper.get_logout_url(
            'foo_token', self.REDIRECT_URL)
        expected_url = 'https://www.facebook.com/logout.php?'
        self.assertTrue(
            logout_url.startswith(expected_url),
            'Unexpected base logout URL returned from get_logout_url().')

        params = {
            'next': self.REDIRECT_URL,
            'access_token': 'foo_token'
        }

        for key, value in params.items():
            self.assertIn('{}={}'.format(key, quote_plus(value)),
                          logout_url,
                          '{}={} not found in logout_url'.format(
                              key, quote_plus(value)))

    def test_an_access_token_can_be_obtained_from_redirect(self):
        self.persistent_data_handler.set('state', 'foo_state')

        get_params = {
            'state': 'foo_state',
            'code': 'foo_code'
        }
        access_token = self.redirect_login_helper.get_access_token(
            get_params, self.REDIRECT_URL)

        self.assertEqual('foo_token_from_code|foo_code|' + self.REDIRECT_URL,
                         access_token)

    def test_a_custom_csprsg_can_be_injected(self):
        app = FacebookApp('123', 'foo_app_secret')
        access_token_client = FooRedirectLoginOAuth2Client(app,
                                                           FacebookClient(),
                                                           'v1337')
        foo_prsg = FooPseudoRandomStringGenerator()
        helper = FacebookRedirectLoginHelper(access_token_client,
                                             self.persistent_data_handler,
                                             None, foo_prsg)

        login_url = helper.get_login_url(self.REDIRECT_URL)
        self.assertIn('state=csprs123', login_url)

    def test_the_pseudo_random_string_generator_will_auto_detect_csprsg(self):
        self.assertIsInstance(
            self.redirect_login_helper.get_pseudo_random_string_generator(),
            UrandomPseudoRandomStringGenerator)
