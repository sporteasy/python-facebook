from python_facebook.sdk.authentication.oauth2_client import OAuth2Client


class FooRedirectLoginOAuth2Client(OAuth2Client):

    def get_access_token_from_code(self, code, redirect_uri='', machine_id=None):
        return 'foo_token_from_code|' + code + '|' + redirect_uri
