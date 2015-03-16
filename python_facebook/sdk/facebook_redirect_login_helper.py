# -*- coding: utf-8 -*-
import urllib
import os

from python_facebook.sdk.request import FacebookRequest
from python_facebook.sdk.session import FacebookSession


class FacebookRedirectLoginHelper(object):
    """
    Inspired by Facebook PHP SDK
    """

    SESSION_PREFIX = 'FBRLH_'

    def __init__(self, redirect_url, app_id=None, app_secret=None):
        """
        Constructs a RedirectLoginHelper for a given appId and redirectUrl.

        :param redirect_url: The URL Facebook should redirect users to after login
        :param app_id: The application id
        :param app_secret: The application secret
        """
        self.app_id = FacebookSession.get_target_app_id(app_id)
        self.app_secret = FacebookSession.get_target_app_secret(app_secret)
        self.redirect_url = redirect_url
        self.state = None
        self.check_for_session_status = True
        self.session = {}

    def get_login_url(self, scope=None, version=None, display_as_popup=False, auth_type=False):
        """
        Stores CSRF state and returns a URL to which the user should be sent to
        in order to continue the login process with Facebook.  The
        provided redirectUrl should invoke the handleRedirect method.

        :param scope: List of permissions to request during login
        :param version: Optional Graph API version if not default (v2.0)
        :param display_as_popup: Indicate if the page will be displayed as a popup
        :param boolean|string auth_type: 'reauthenticate' or 'https', true is equivalent
                                          to 'reauthenticate', false or invalid value
                                          will not add auth type parameter
        :return: string url
        """
        scope = scope or []
        version = version or FacebookRequest.GRAPH_API_VERSION
        self.state = self.random(16)
        self._store_state(self.state)

        params = {
            'client_id': self.app_id,
            'redirect_uri': self.redirect_url,
            'state': self.state,
            # 'sdk': 'python-sdk',
            'scope': ','.join(scope)
        }

        if auth_type in [True, 'reauthenticate', 'https']:
            params.update({'auth_type': 'reauthenticate' if auth_type is True else auth_type})

        if display_as_popup:
            params.update({'display': 'popup'})

        return 'https://www.facebook.com/' + version + '/dialog/oauth?' + urllib.urlencode(params)

    def get_re_request_url(self, scope, version=None):
        """
        Returns a URL to which the user should be sent to re-request permissions.
        :param scope: List of permissions to re-request
        :param version: Optional Graph API version if not default (v2.0)
        :return: string url
        """
        pass

    def get_logout_url(self, session, next):
        params = {
            'next': next,
            'access_token': session.get_token()
        }
        return 'https://www.facebook.com/logout.php?' + urllib.urlencode(params)

    def get_session_from_redirect(self, code, state):
        """
        Handles a response from Facebook, including a CSRF check, and returns a FacebookSession

        :return: @return FacebookSession|null
        """
        if self._is_valid_redirect(code, state):
            params = {
                'client_id': FacebookSession.get_target_app_id(self.app_id),
                'redirect_uri': self.redirect_url,
                'client_secret': FacebookSession.get_target_app_secret(self.app_secret),
                'code': code
            }
            response = FacebookRequest(
                self.app_id,
                self.app_secret,
                FacebookSession.new_app_session(self.app_id, self.app_secret),
                'GET',
                '/oauth/access_token',
                params
            ).execute().response_data
            if 'access_token' in response:
                return FacebookSession(response['access_token'])
        return None

    def _is_valid_redirect(self, code, state):
        """
        Check if a redirect has a valid state.

        :return boolean:
        """
        if not code or not state:
            return False

        saved_state = self._load_state()
        if len(state) != len(saved_state):
            return False

        return state == saved_state

    def _store_state(self, state):
        self.session[self.SESSION_PREFIX + 'state'] = state

    def _load_state(self):
        """
        Loads a state string from session storage for CSRF validation.  May return
        null if no object exists.  Developers should subclass and override this
        method if they want to load the state from a different location.

        :return string|None:
        """
        self.state = self.session.get(self.SESSION_PREFIX + 'state', None)
        return self.state

    def random(self, bytes):
        """
        Generate a cryptographically secure pseudorandom number

        :param int bytes: number of bytes to return
        :return string:
        """
        return os.urandom(bytes).encode('hex')

    def disable_session_status_check(self):
        """
        Disables the session_status()
        """
        self.check_for_session_status = False


class DjangoFacebookRedirectLoginHelper(FacebookRedirectLoginHelper):

    def __init__(self, redirect_url, session, app_id=None, app_secret=None):
        super(DjangoFacebookRedirectLoginHelper, self).__init__(redirect_url, app_id, app_secret)
        self.session = session
