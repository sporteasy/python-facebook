import datetime
import time

from tests import PythonFacebookTestCase
from python_facebook.sdk.authentication.access_token_metadata import AccessTokenMetadata
from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException


class AccessTokenMetadataTestCase(PythonFacebookTestCase):
    graph_response_data = {
        'data': {
            'app_id': '123',
            'application': 'Foo App',
            'error': {
                'code': 190,
                'message': 'Foo error message.',
                'subcode': 463
            },
            'issued_at': 1422110200,
            'expires_at': 1422115200,
            'is_valid': False,
            'metadata': {
                'sso': 'iphone-sso',
                'auth_type': 'rerequest',
                'auth_nonce': 'no-replicatey'
            },
            'scopes': ['public_profile', 'basic_info', 'user_friends'],
            'profile_id': '1000',
            'user_id': '1337'
        }
    }

    def test_dates_get_cast_to_date_time(self):
        metadata = AccessTokenMetadata(self.graph_response_data)

        expires = metadata.get_expires_at()
        issued_at = metadata.get_issued_at()

        self.assertIsInstance(expires, datetime.datetime)
        self.assertIsInstance(issued_at, datetime.datetime)

    def test_all_the_getters_return_the_proper_value(self):
        metadata = AccessTokenMetadata(self.graph_response_data)

        self.assertEqual('123', metadata.get_app_id())
        self.assertEqual('Foo App', metadata.get_application())
        self.assertTrue(metadata.is_error(), 'Expected an error')
        self.assertEqual('190', metadata.get_error_code())
        self.assertEqual('Foo error message.', metadata.get_error_message())
        self.assertEqual('463', metadata.get_error_subcode())
        self.assertFalse(metadata.get_is_valid(), 'Expected the access token to not be valid')
        self.assertEqual('iphone-sso', metadata.get_sso())
        self.assertEqual('rerequest', metadata.get_auth_type())
        self.assertEqual('no-replicatey', metadata.get_auth_nonce())
        self.assertEqual('1000', metadata.get_profile_id())
        self.assertEqual(['public_profile', 'basic_info', 'user_friends'], metadata.get_scopes())
        self.assertEqual('1337', metadata.get_user_id())

    def test_invalid_metadata_will_throw(self):
        with self.assertRaises(FacebookSDKException):
            AccessTokenMetadata({'foo': 'bar'})

    def test_an_expected_app_id_will_not_throw(self):
        access_token = AccessTokenMetadata(self.graph_response_data)
        access_token.validate_app_id('123')

    def test_an_unexpected_app_id_will_throw(self):
        access_token = AccessTokenMetadata(self.graph_response_data)
        with self.assertRaises(FacebookSDKException):
            access_token.validate_app_id('foo')

    def test_an_expected_user_id_will_not_throw(self):
        access_token = AccessTokenMetadata(self.graph_response_data)
        access_token.validate_user_id('1337')

    def test_an_unexpected_user_id_will_throw(self):
        access_token = AccessTokenMetadata(self.graph_response_data)
        with self.assertRaises(FacebookSDKException):
            access_token.validate_user_id('foo')

    def test_an_active_access_token_will_not_throw(self):
        graph_response_data = self.graph_response_data.copy()
        graph_response_data['data']['expires_at'] = time.time() + 1000
        access_token = AccessTokenMetadata(graph_response_data)
        access_token.validate_expiration()

    def test_an_expired_access_token_will_throw(self):
        graph_response_data = self.graph_response_data.copy()
        graph_response_data['data']['expires_at'] = time.time() - 1000
        access_token = AccessTokenMetadata(graph_response_data)
        with self.assertRaises(FacebookSDKException):
            access_token.validate_expiration()
