# -*- coding: utf-8 -*-
from python_facebook.access_token import AccessToken


class FacebookSession(object):

    DEFAULT_APP_ID = None

    DEFAULT_APP_SECRET = None

    USE_APP_SECRET_PROOF = True

    def __init__(self, access_token, signed_request=None):
        """
        When creating a Session from an access_token, use:
        session = FacebookSession(access_token);
        This will validate the token and provide a Session object ready for use.
        It will throw a SessionException in case of error.

        :param access_token:
        :param signed_request:
        :return:
        """
        if isinstance(access_token, AccessToken):
            self.access_token = access_token
        else:
            self.access_token = AccessToken(access_token)
        self.signed_request = signed_request

    def get_token(self):
        """
        Returns the access token.

        :return string access_token:
        """
        return self.access_token.access_token

    def get_signed_request_data(self):
        return self.signed_request.get_payload() if self.signed_request else None

    def get_signed_request_property(self, key):
        return self.signed_request.get(key) if self.signed_request else None

    def get_user_id(self):
        return self.signed_request.get_user_id() if self.signed_request else None

    def get_session_info(self, app_id=None, app_secret=None):
        return self.access_token.get_info(app_id, app_secret)

    def get_long_lived_session(self, app_id=None, app_secret=None):
        """
        Returns a new Facebook session resulting from
        extending a short-lived access token.

        :param app_id:
        :param app_secret:
        :return FacebookSession:
        """
        long_lived_access_token = self.access_token.extend(app_id, app_secret)
        return FacebookSession(long_lived_access_token, self.signed_request)

    def get_exchange_token(self, app_id=None, app_secret=None):
        """
        Returns an exchange token string which can be sent
        back to clients and exchanged for a device-linked access token.

        :param app_id:
        :param app_secret:
        :return string:
        """
        return AccessToken.get_code_from_access_token(self.access_token, app_id, app_secret)

    def validate(self, app_id=None, app_secret=None, machine_id=None):
        pass

    @staticmethod
    def validate_session_info(token_info, app_id=None, machine_id=None):
        pass

    @staticmethod
    def new_session_from_signed_request(signed_request):
        pass

    @staticmethod
    def new_session_after_validation(signed_request):
        pass

    @classmethod
    def new_app_session(cls, app_id=None, app_secret=None):
        """
        Returns a FacebookSession configured with a token for the
        application which can be used for publishing and requesting app-level
        information.

        :param app_id:
        :param app_secret:
        :return FacebookSession:
        """
        target_app_id = cls.get_target_app_id(app_id)
        target_app_secret = cls.get_target_app_secret(app_secret)
        return cls(target_app_id + '|' + target_app_secret)

    @classmethod
    def set_default_application(cls, app_id, app_secret):
        cls.DEFAULT_APP_ID = app_id
        cls.DEFAULT_APP_SECRET = app_secret

    @classmethod
    def get_target_app_id(cls, app_id=None):
        """
        Will return either the provided app Id or the default,
        throwing if neither are populated.

        :param app_id:
        :return:
        :raise FacebookException:
        """
        target = app_id or cls.DEFAULT_APP_ID
        if not target:
            from python_facebook.exceptions import FacebookException
            raise FacebookException('You must provide or set a default application id.', 700)
        return target

    @classmethod
    def get_target_app_secret(cls, app_secret=None):
        """
        Will return either the provided app secret or the
        default, throwing if neither are populated.

        :param app_secret:
        :return:
        :raise FacebookException:
        """
        target = app_secret or cls.DEFAULT_APP_SECRET
        if not target:
            from python_facebook.exceptions import FacebookException
            raise FacebookException('You must provide or set a default application secret.', 701)
        return target

    @classmethod
    def enable_app_secret_proof(cls, on=True):
        cls.USE_APP_SECRET_PROOF = True if on is True else False

    @classmethod
    def use_app_secret_proof(cls):
        return cls.USE_APP_SECRET_PROOF
