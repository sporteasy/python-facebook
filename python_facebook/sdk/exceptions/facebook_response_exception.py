# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from python_facebook.sdk.exceptions.facebook_authentication_exception import FacebookAuthenticationException
from python_facebook.sdk.exceptions.facebook_authorization_exception import FacebookAuthorizationException
from python_facebook.sdk.exceptions.facebook_client_exception import FacebookClientException
from python_facebook.sdk.exceptions.facebook_resumable_upload_exception import FacebookResumableUploadException
from python_facebook.sdk.exceptions.facebook_other_exception import FacebookOtherException
from python_facebook.sdk.exceptions.facebook_server_exception import FacebookServerException
from python_facebook.sdk.exceptions.facebook_throttle_exception import FacebookThrottleException
from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException

# Error codes
OTHER_AUTHENTICATION_ERROR_CODES = (458, 459, 460, 463, 464, 467)
VIDEO_UPLOAD_RESUMABLE_ERROR_CODES = (1363030, 1363019, 1363037, 1363033, 1363021, 1363041)
LOGIN_ERROR_CODES = (100, 102, 190 )    # Login status or token expired, revoked, or invalid
SERVER_ERROR_CODES = (1, 2)
API_THROTTLING_ERROR_CODES = (4, 17, 341)
DUPLICATE_POST_ERROR_CODES = (506, )


class FacebookResponseException(FacebookSDKException):

    def __init__(self, response, previous_exception=None):
        self.response = response
        self.response_data = response.get_decoded_body()
        self.previous_exception = previous_exception

        super(FacebookResponseException, self).__init__(
            self.__get('message', 'Unknown error from Graph.'),
            self.__get('code', -1)
        )

    def get_previous(self):
        return self.previous_exception

    @classmethod
    def create(self, response):
        data = response.get_decoded_body()

        if not ('error' in data and 'code' in data['error']) and 'code' in data:
            data = {
                'error': data
            }

        code = data['error'].get('code', None)
        message = data['error'].get('message', 'Unknown error from Graph.')

        if data['error']['error_subcode']:
            if data['error']['error_subcode'] in OTHER_AUTHENTICATION_ERROR_CODES:
                return FacebookResponseException(response, FacebookAuthenticationException(message, code))
            elif data['error']['error_subcode'] in VIDEO_UPLOAD_RESUMABLE_ERROR_CODES:
                return FacebookResponseException(response, FacebookResumableUploadException(message, code))

        if code in LOGIN_ERROR_CODES:
            return FacebookResponseException(response, FacebookAuthenticationException(message, code))
        elif code in SERVER_ERROR_CODES:
            return FacebookResponseException(response, FacebookServerException(message, code))
        elif code in API_THROTTLING_ERROR_CODES:
            return FacebookResponseException(response, FacebookThrottleException(message, code))
        elif code in DUPLICATE_POST_ERROR_CODES:
            return FacebookResponseException(response, FacebookClientException(message, code))

        # Missing permissions
        if code == 10 or 200 <= code <= 299:
            return FacebookResponseException(response, FacebookAuthorizationException(message, code))

        # OAuth authentication error
        elif data['error'].get('type', '') == 'OAuthException':
            return FacebookResponseException(response, FacebookAuthenticationException(message, code))

        # All others
        return FacebookResponseException(response, FacebookOtherException(message, code))

    def __get(self, key, default=None):
        if 'error' in self.response_data and key in self.response_data['error']:
            return self.response_data['error'][key]
        return default

    def get_http_status_code(self):
        return self.response.get_http_status_code()

    def get_sub_error_code(self):
        return self.__get('error_subcode', -1)

    def get_error_type(self):
        return self.__get('type', '')

    def get_raw_response(self):
        return self.response.get_body()

    def get_response_data(self):
        return self.response

    def get_response(self):
        return self.response_data
