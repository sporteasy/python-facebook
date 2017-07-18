import unittest

from python_facebook.sdk.authentication.access_token import AccessToken


class AccessTokenTest(unittest.TestCase):

    def test_an_access_token_can_be_returned_as_astring(self):
        access_token = AccessToken('foo_token')

        self.assertEqual('foo_token', access_token.get_value())
        self.assertEqual('foo_token', access_token)

    def test_an_app_secret_proof_will_be_properly_generated(self):
        access_token = AccessToken('foo_token')

        app_secret_proof = access_token.get_app_secret_proof('shhhhh!is.my.secret')
        self.assertEqual('796ba0d8a6b339e476a7b166a9e8ac0a395f7de736dc37de5f2f4397f5854eb8',
                         app_secret_proof)

    def test_an_app_access_token_can_be_detected(self):
        normal_token = AccessToken('foo_token')
        is_normal_token = normal_token.is_app_access_token()

        self.assertFalse(is_normal_token, 'Normal access token not expected to look like an app access token.')

        app_token = AccessToken('123|secret')
        is_app_token = app_token.is_app_access_token()
        
        self.assertTrue(is_app_token, 'App access token expected to look like an app access token.')
