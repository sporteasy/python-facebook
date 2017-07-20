try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from python_facebook.sdk.authentication.access_token import AccessToken
from python_facebook.sdk.exceptions.facebook_sdk_exception import \
    FacebookSDKException
from python_facebook.sdk.persistent_data.\
    facebook_memory_persistent_data_handler import \
    FacebookMemoryPersistentDataHandler
from python_facebook.sdk.pseudo_random_string.\
    pseudo_random_string_generator_factory import \
    PseudoRandomStringGeneratorFactory as PRSGF
from python_facebook.sdk.url.facebook_url_detection_handler import \
    FacebookUrlDetectionHandler
from python_facebook.sdk.url.facebook_url_manipulator import \
    FacebookUrlManipulator
from python_facebook.sdk.utils import constant_time_compare


class FacebookRedirectLoginHelper(object):
    CSRF_LENGTH = 32

    def __init__(self, oauth2_client, persistent_data_handler=None,
                 url_handler=None, prsg=None):
        self.oauth2_client = oauth2_client
        self.persistent_data_handler = persistent_data_handler or \
            FacebookMemoryPersistentDataHandler()
        self.url_detection_handler = url_handler or \
            FacebookUrlDetectionHandler()
        self.pseudo_random_string_generator = PRSGF.\
            create_pseudo_random_string_generator(prsg)

    def get_persistent_data_handler(self):
        return self.persistent_data_handler

    def get_url_detection_handler(self):
        return self.url_detection_handler

    def get_pseudo_random_string_generator(self):
        return self.pseudo_random_string_generator

    def make_url(self, redirect_url, scope, params=None, separator='&'):
        """
        Stores CSRF state and returns a URL to which the user should be sent
        to in order to continue the login
        process with Facebook.
        """
        state = self.persistent_data_handler.get('state')
        if not state:
            state = self.pseudo_random_string_generator.\
                get_pseudo_random_string(self.CSRF_LENGTH)

        self.persistent_data_handler.set('state', state)

        return self.oauth2_client.get_authorization_url(redirect_url, state,
                                                        scope, params,
                                                        separator)

    def get_login_url(self, redirect_url, scope=None, separator='&'):
        """
        Returns the URL to send the user in order to login to Facebook.
        """
        return self.make_url(redirect_url, scope, [], separator)

    def get_logout_url(self, access_token, next, separator='&'):
        """
        Returns the URL to send the user in order to log out of Facebook.
        """
        if not isinstance(access_token, AccessToken):
            access_token = AccessToken(access_token)

        if access_token.is_app_access_token():
            raise FacebookSDKException(
                'Cannot generate a logout URL with an app access token.', 722)

        params = {
            'next': next,
            'access_token': access_token.get_value()
        }

        return 'https://www.facebook.com/logout.php?' + urlencode(
            sorted(params.items()))

    def get_re_request_url(self, redirect_url, scope=None, separator='&'):
        """
        Returns the URL to send the user in order to login to Facebook
        with permission(s) to be re-asked.
        """
        params = {
            'auth_type': 'rerequest'
        }
        return self.make_url(redirect_url, scope, params, separator)

    def get_re_authentication_url(self, redirect_url, scope=None,
                                  separator='&'):
        """
        Returns the URL to send the user in order to login to Facebook
        with user to be re-authenticated.
        """
        params = {
            'auth_type': 'reauthenticate'
        }
        return self.make_url(redirect_url, scope, params, separator)

    def get_access_token(self, get_params, redirect_url=None):
        """
        Takes a valid code from a login redirect, and returns an
        AccessToken entity.
        """
        code = self.get_code(get_params)

        if not code:
            return None

        self.validate_csrf(get_params)
        self.reset_csrf()

        redirect_url = redirect_url or \
            self.url_detection_handler.get_current_url()
        # At minimum we need to remove the state param
        redirect_url = FacebookUrlManipulator.remove_params_from_url(
            redirect_url, ['state'])

        return self.oauth2_client.get_access_token_from_code(code,
                                                             redirect_url)

    def validate_csrf(self, get_params):
        """
        Validate the request against a cross-site request forgery.
        """
        state = self.get_state(get_params)
        if not state:
            raise FacebookSDKException(
                'Cross-site request forgery validation failed. '
                'Required GET param "state" missing.')

        saved_state = self.persistent_data_handler.get('state')
        if not saved_state:
            raise FacebookSDKException(
                'Cross-site request forgery validation failed. '
                'Required param "state" missing from persistent data.')

        if constant_time_compare(saved_state, state):
            return None

        raise FacebookSDKException(
            'Cross-site request forgery validation failed. '
            'The "state" param from the URL and session do not match.')

    def reset_csrf(self):
        self.persistent_data_handler.set('state', None)

    def get_code(self, get_params):
        return self.get_input(get_params, 'code')

    def get_state(self, get_params):
        return self.get_input(get_params, 'state')

    def get_error_code(self, get_params):
        return self.get_input(get_params, 'error_code')

    def get_error(self, get_params):
        return self.get_input(get_params, 'error')

    def get_error_reason(self, get_params):
        return self.get_input(get_params, 'error_reason')

    def get_error_description(self, get_params):
        return self.get_input(get_params, 'error_description')

    def get_input(self, get_params, key):
        """
        Returns a value from a GET param.
        """
        return get_params.get(key)
