from python_facebook.sdk.authentication.access_token import AccessToken


class FacebookApp(object):

    def __init__(self, id, secret):
        self.id = id
        self.secret = secret

    def get_id(self):
        return self.id

    def get_secret(self):
        return self.secret

    def get_access_token(self):
        """
        Returns an app access token.
        """
        return AccessToken(self.id + '|' + self.secret)

    def serialize(self):
        """
        Serializes the FacebookApp entity as a string.
        """
        return '|'.join([self.id, self.secret])

    def unserialize(self):
        raise NotImplementedError
