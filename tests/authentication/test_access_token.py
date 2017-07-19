import time
from unittest import skip

from tests import PythonFacebookTestCase
from python_facebook.sdk.authentication.access_token import AccessToken


class AccessTokenTestCase(PythonFacebookTestCase):
    def _get_a_week_from_now(self):
        return time.time() + (60 * 60 * 24 * 7)

    def test_an_access_token_can_be_returned_as_astring(self):
        access_token = AccessToken('foo_token')

        self.assertEqual('foo_token', access_token.get_value())
        self.assertEqual('foo_token', str(access_token))

    def test_an_app_secret_proof_will_be_properly_generated(self):
        access_token = AccessToken('foo_token')

        app_secret_proof = access_token.get_app_secret_proof(
            'shhhhh!is.my.secret')
        self.assertEqual(
            '796ba0d8a6b339e476a7b166a9e8ac0a395f7de736dc37de5f2f4397f5854eb8',
            app_secret_proof)

    def test_an_app_access_token_can_be_detected(self):
        normal_token = AccessToken('foo_token')
        is_normal_token = normal_token.is_app_access_token()

        self.assertFalse(
            is_normal_token,
            'Normal access token not expected to look like an app access '
            'token.')

        app_token = AccessToken('123|secret')
        is_app_token = app_token.is_app_access_token()

        self.assertTrue(
            is_app_token,
            'App access token expected to look like an app access token.')

    def test_short_lived_access_tokens_can_be_detected(self):
        an_hour_and_ahalf = time.time() + 1.5 * 60
        access_token = AccessToken('foo_token', an_hour_and_ahalf)

        is_long_lived = access_token.is_long_lived()
        self.assertFalse(is_long_lived,
                         'Expected access token to be short lived.')

    def test_long_lived_access_tokens_can_be_detected(self):
        access_token = AccessToken('foo_token', self._get_a_week_from_now())

        is_long_lived = access_token.is_long_lived()
        self.assertTrue(is_long_lived,
                        'Expected access token to be long lived.')

    def test_an_app_access_token_does_not_expire(self):
        app_token = AccessToken('123|secret')
        has_expired = app_token.is_expired()

        self.assertFalse(has_expired,
                         'App access token not expected to expire.')

    def test_an_access_token_can_expire(self):
        expire_time = time.time() - 100
        app_token = AccessToken('foo_token', expire_time)

        has_expired = app_token.is_expired()
        self.assertTrue(has_expired,
                        'Expected 100 second old access token to be expired.')

    @skip
    def test_access_token_can_be_serialized(self):
        access_token = AccessToken('foo', time.time())
        raise NotImplementedError
