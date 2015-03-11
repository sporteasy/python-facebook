# -*- coding: utf-8 -*-


class FacebookException(Exception):
    pass


class FacebookRequestException(FacebookException):

    def __init__(self, raw_response, response_data, status_code):
        self.raw_response = raw_response
        self.response_data = response_data
        self.status_code = status_code
        super(FacebookRequestException, self).__init__(raw_response)

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
