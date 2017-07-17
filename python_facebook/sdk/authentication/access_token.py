# -*- coding: utf-8 -*-
import hashlib
import hmac

from datetime import datetime, timedelta


class AccessToken(object):

    def __init__(self, access_token, expires_at=0):
        """
        Create a new access token entity.

        :param access_token:
        :param expires_at:
        """
        self.value = access_token
        self.expires_at = None
        if expires_at:
            self.set_expires_at_from_timestamp(expires_at)

    def __unicode__(self):
        return self.value

    def __str__(self):
        return self.value

    def get_app_secret_proof(self, app_secret):
        hmac.new(app_secret, self.value, hashlib.sha256).hexdigest()

    def get_expires_at(self):
        return self.expires_at

    def is_app_access_token(self):
        return '|' not in self.value

    def is_long_lived(self):
        """
        Determines whether or not this is a long-lived token.

        :return: boolean
        """
        if self.expires_at:
            return self.expires_at > datetime.now() + timedelta(2)

        if self.is_app_access_token():
            return True

        return False

    def is_expired(self):
        if isinstance(self.get_expires_at(), datetime):
            return self.get_expires_at() < datetime.now()

        if self.is_app_access_token():
            return False

        return None

    def get_value(self):
        return self.value

    def set_expires_at_from_timestamp(self, timestamp):
        self.expires_at = datetime.fromtimestamp(timestamp)
