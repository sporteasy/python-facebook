# -*- coding: utf-8 -*-


class FacebookSDKException(Exception):

    def __init__(self, message, code=None):
        self.message = message
        self.code = code
        super(FacebookSDKException, self).__init__(message)


class FacebookRequestException(FacebookSDKException):

    def __init__(self, raw_response, response_data, status_code):
        self.raw_response = raw_response
        self.response_data = response_data
        self.status_code = status_code
        super(FacebookRequestException, self).__init__(
            self.__get('message', 'Unknown Exception'),
            self.__get('code', -1)
        )
        self.sub_error_code = self.__get('error_subcode', -1)
        self.error_type = self.__get('type', '')

    def __get(self, key, default=None):
        """
        Checks isset and returns that or a default value.

        :param key:
        :param default:
        :return:
        """
        if 'error' in self.response_data and key in self.response_data['error']:
            return self.response_data['error'][key]
        return default

    @classmethod
    def create(cls, raw, data, status_code):
        """
        Process an error payload from the Graph API and return the appropriate
        exception subclass.

        :param raw: the raw response from the Graph API
        :param data: the decoded response from the Graph API
        :param status_code: the HTTP response code
        :return FacebookRequestException:
        """
        if not ('error' in data and 'code' in data['error']) and 'code' in data:
            data = {
                'error': data
            }

        code = None
        if data.get('error') and data['error'].get('code'):
            code = int(data['error']['code'])

        if data.get('error') and data['error'].get('error_subcode'):
            code = data['error']['error_subcode']

            if code == 458 or \
                    code == 459 or \
                    code == 460 or \
                    code == 463 or \
                    code == 464 or \
                    code == 467:
                # Other authentication issues
                return FacebookAuthorizationException(raw, data, status_code)

        if code == 100 or \
                code == 102 or \
                code == 190:
            # Login status or token expired, revoked, or invalid
            return FacebookAuthorizationException(raw, data, status_code)

        elif code == 1 or \
                code == 2:
            # Server issue, possible downtime
            return FacebookServerException(raw, data, status_code)

        elif code == 4 or \
                code == 17 or \
                code == 341:
            # API Throttling
            return FacebookThrottleException(raw, data, status_code)

        elif code == 506:
            # Duplicate Post
            return FacebookClientException(raw, data, status_code)

        # Missing Permissions
        elif code == 10 or (code >= 200 and code <= 299):
            return FacebookPermissionException(raw, data, status_code)

        # OAuth authentication error
        elif data.get('error') and data['error'].get('type') \
                and data['error']['type'] == 'OAuthException':
            return FacebookAuthorizationException(raw, data, status_code)

        return FacebookOtherException(raw, data, status_code)


class FacebookServerException(FacebookRequestException):
    pass


class FacebookClientException(FacebookRequestException):
    pass


class FacebookThrottleException(FacebookRequestException):
    pass


class FacebookAuthorizationException(FacebookRequestException):
    pass


class FacebookPermissionException(FacebookRequestException):
    pass


class FacebookOtherException(FacebookRequestException):
    pass
