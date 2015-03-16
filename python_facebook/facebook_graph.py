# -*- coding: utf-8 -*-
from python_facebook.sdk.entities.access_token import AccessToken
from python_facebook.sdk.graph_user import GraphUser
from python_facebook.sdk.facebook_redirect_login_helper import FacebookRedirectLoginHelper
from python_facebook.sdk.request import FacebookRequest
from python_facebook.sdk.session import FacebookSession


class FacebookGraph(object):
    """
    Helper for very simple usage of the SDK
    """
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

        self.access_token = None
        self.session = None

    def set_access_token(self, access_token, expires_at=0, machine_id=None):
        self.access_token = AccessToken(access_token, expires_at, machine_id)

    def get_access_token_info(self):
        return self.access_token.get_info(self.app_id, self.app_secret)

    def get_login_url(self, redirect_url):
        fbrlh = FacebookRedirectLoginHelper(redirect_url, self.app_id, self.app_secret)
        return fbrlh.get_login_url()

    def set_session_from_redirect(self, redirect_url, code, state):
        fbrlh = FacebookRedirectLoginHelper(redirect_url, self.app_id, self.app_secret)
        self.session = fbrlh.get_session_from_redirect(code, state)

    def get_graph_user(self):
        if self.session is None:
            self.session = FacebookSession(self.access_token)

        return FacebookRequest(
            self.app_id,
            self.app_secret,
            self.session,
            'GET',
            '/me'
        ).execute().get_graph_object(GraphUser)
