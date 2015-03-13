# -*- coding: utf-8 -*-
import time

from datetime import datetime, timedelta

from python_facebook.exceptions import FacebookRequestException
from python_facebook.graph_session_info import GraphSessionInfo


class AccessToken(object):

    def __init__(self, access_token, expires_at=0, machine_id=None):
        """
        Create a new access token entity.

        :param access_token:
        :param expires_at:
        :param machine_id:
        :return:
        """
        self.access_token = access_token
        self.expires_at = None
        if expires_at:
            self.set_expires_at_from_timestamp(expires_at)
        self.machine_id = machine_id

    def __unicode__(self):
        return self.access_token

    def set_expires_at_from_timestamp(self, timestamp):
        self.expires_at = datetime.fromtimestamp(timestamp)

    def is_long_lived(self):
        """
        Determines whether or not this is a long-lived token.

        :return: boolean
        """
        if self.expires_at:
            return self.expires_at > datetime.now() + timedelta(2)
        return False

    def is_valid(self, app_id=None, app_secret=None, machine_id=None):
        """
        Checks the validity of the access token.

        :param string|null app_id: Application ID to use
        :param string|null app_secret:
        :param string|null machine_id:
        :return boolean:
        """
        access_token_info = self.get_info(app_id, app_secret)
        machine_id = machine_id or self.machine_id
        return self.validate_access_token(access_token_info, app_id, machine_id)

    @staticmethod
    def validate_access_token(token_info, app_id=None, machine_id=None):
        """
        Ensures the provided GraphSessionInfo object is valid,
        throwing an exception if not.  Ensures the appId matches,
        that the machineId matches if it's being used,
        that the token is valid and has not expired.

        :param token_info:
        :param app_id:
        :param machine_id:

        :return boolean:
        """
        from python_facebook.session import FacebookSession

        target_app_id = FacebookSession.get_target_app_id(app_id)

        app_is_valid = token_info.app_id == target_app_id
        machine_id_is_valid = token_info.machine_id == machine_id
        access_token_is_valid = token_info.is_valid

        access_token_is_still_alive = True
        # Not all access tokens return an expiration. E.g. an app access token
        if isinstance(token_info.expires_at, datetime):
            access_token_is_still_alive = token_info.expires_at >= datetime.now()

        return app_is_valid and machine_id_is_valid and access_token_is_valid \
            and access_token_is_still_alive

    def get_info(self, app_id=None, app_secret=None):
        from python_facebook.request import FacebookRequest
        from python_facebook.session import FacebookSession

        params = {
            'input_token': self.access_token
        }
        request = FacebookRequest(
            FacebookSession.new_app_session(app_id, app_secret),
            'GET',
            '/debug_token',
            params
        )
        response = request.execute().get_graph_object(GraphSessionInfo)

        if response.expires_at:
            self.expires_at = response.expires_at

        return response

    @classmethod
    def get_access_token_from_code(cls, code, app_id=None, app_secret=None, machine_id=None):
        """
        Get a valid access token from a code.

        :param code:
        :param app_id:
        :param app_secret:
        :param machine_id:

        :return AccessToken:
        """
        params = {
            'code': code,
            'redirect_uri': ''
        }

        if machine_id:
            params['machine_id'] = machine_id

        return cls.request_access_token(params, app_id, app_secret)

    @classmethod
    def get_code_from_access_token(cls, access_token, app_id=None, app_secret=None):
        """
        Get a valid code from an access token.

        :param access_token:
        :param app_id:
        :param app_secret:

        :return AccessToken:
        """
        access_token = str(access_token)
        params = {
            'access_token': access_token,
            'redirect_uri': ''
        }
        return cls.request_code(params, app_id, app_secret)

    def extend(self, app_id=None, app_secret=None):
        """
        Exchanges a short lived access token with a long lived access token

        :param app_id:
        :param app_secret:

        :return AccessToken:
        """
        params = {
            'grant_type': 'fb_exchange_token',
            'fb_exchange_token': self.access_token
        }
        return self.request_access_token(params, app_id, app_secret)

    @classmethod
    def request_access_token(cls, params, app_id=None, app_secret=None):
        """
        Request an access token based on a set of params.

        :param params:
        :param app_id:
        :param app_secret:

        :return AccessToken:
        """
        response = cls.request('/oauth/access_token', params, app_id, app_secret)
        data = response.response_data

        if isinstance(data, dict):
            if 'access_token' in data:
                expires_at = time.time() + data['expires'] if 'expires' in data else 0
                return AccessToken(data['access_token'], expires_at)

        # todo: missing code here

        raise FacebookRequestException.create(
            response.raw_response,
            data,
            401
        )

    @classmethod
    def request_code(cls, params, app_id=None, app_secret=None):
        response = cls.request('/oauth/client_code', params, app_id, app_secret)
        data = response.response_data

        if 'code' in data:
            return data['code']

        raise FacebookRequestException.create(
            response.raw_response,
            data,
            401
        )

    @classmethod
    def request(cls, endpoint, params, app_id=None, app_secret=None):
        """
        Send a request to Graph with an app access token.

        :return FacebookResponse:
        """
        from python_facebook.session import FacebookSession
        from python_facebook.request import FacebookRequest

        target_app_id = FacebookSession.get_target_app_id(app_id)
        target_app_secret = FacebookSession.get_target_app_id(app_secret)

        if not params.get('client_id'):
            params['client_id'] = target_app_id
        if not params.get('client_secret'):
            params['client_secret'] = target_app_secret

        # The response for this endpoint is not JSON, so it must be handled
        # differently, not as a GraphObject.
        request = FacebookRequest(
            FacebookSession.new_app_session(target_app_id, target_app_secret),
            'GET',
            endpoint,
            params
        )
        return request.execute()

    def is_app_session(self):
        """
        Returns true if the access token is an app session token.

        :return boolean:
        """
        return '|' in self.access_token
