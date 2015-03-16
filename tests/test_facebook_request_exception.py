# -*- coding: utf-8 -*-
import unittest
import json

from python_facebook.sdk.exceptions import (
    FacebookRequestException,
    FacebookAuthorizationException,
    FacebookServerException,
    FacebookThrottleException,
    FacebookPermissionException,
    FacebookClientException,
    FacebookOtherException,
    FacebookSDKException
)
from python_facebook.sdk.session import FacebookSession


class TestFacebookRequestException(unittest.TestCase):

    def test_authorization_exceptions(self):
        params = {
            'error': {
                'code': 100,
                'message': 'errmsg',
                'error_subcode': 0,
                'type': 'exception'
            }
        }
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)

        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
        self.assertEqual(100, exception.code)
        self.assertEqual(0, exception.sub_error_code)
        self.assertEqual('exception', exception.error_type)
        self.assertEqual('errmsg', exception.message)
        self.assertEqual(json_str, exception.raw_response)
        self.assertEqual(401, exception.status_code)

        params['error']['code'] = 102
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
        self.assertEqual(102, exception.code)

        params['error']['code'] = 190
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
        self.assertEqual(190, exception.code)

        params['error']['type'] = 'OAuthException'
        params['error']['code'] = 0
        params['error']['error_subcode'] = 458
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
        self.assertEqual(458, exception.sub_error_code)

        params['error']['error_subcode'] = 460
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
        self.assertEqual(460, exception.sub_error_code)

        params['error']['error_subcode'] = 463
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
        self.assertEqual(463, exception.sub_error_code)

        params['error']['error_subcode'] = 467
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
        self.assertEqual(467, exception.sub_error_code)

        params['error']['error_subcode'] = 0
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
        self.assertEqual(0, exception.sub_error_code)

    def test_server_exceptions(self):
        params = {
            'error': {
                'code': 1,
                'message': 'errmsg',
                'error_subcode': 0,
                'type': 'exception'
            }
        }
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 500)

        self.assertTrue(isinstance(exception, FacebookServerException))
        self.assertEqual(1, exception.code)
        self.assertEqual(0, exception.sub_error_code)
        self.assertEqual('exception', exception.error_type)
        self.assertEqual('errmsg', exception.message)
        self.assertEqual(json_str, exception.raw_response)
        self.assertEqual(500, exception.status_code)

        params['error']['code'] = 2
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookServerException))
        self.assertEqual(2, exception.code)

    def test_throttle_exceptions(self):
        params = {
            'error': {
                'code': 4,
                'message': 'errmsg',
                'error_subcode': 0,
                'type': 'exception'
            }
        }
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)

        self.assertTrue(isinstance(exception, FacebookThrottleException))
        self.assertEqual(4, exception.code)
        self.assertEqual(0, exception.sub_error_code)
        self.assertEqual('exception', exception.error_type)
        self.assertEqual('errmsg', exception.message)
        self.assertEqual(json_str, exception.raw_response)
        self.assertEqual(401, exception.status_code)

        params['error']['code'] = 17
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookThrottleException))
        self.assertEqual(17, exception.code)

        params['error']['code'] = 341
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookThrottleException))
        self.assertEqual(341, exception.code)

    def test_user_issue_exceptions(self):
        params = {
            'error': {
                'code': 230,
                'message': 'errmsg',
                'error_subcode': 459,
                'type': 'exception'
            }
        }
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)

        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
        self.assertEqual(230, exception.code)
        self.assertEqual(459, exception.sub_error_code)
        self.assertEqual('exception', exception.error_type)
        self.assertEqual('errmsg', exception.message)
        self.assertEqual(json_str, exception.raw_response)
        self.assertEqual(401, exception.status_code)

        params['error']['code'] = 464
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
        self.assertEqual(464, exception.code)

    def test_permission_exceptions(self):
        params = {
            'error': {
                'code': 10,
                'message': 'errmsg',
                'error_subcode': 0,
                'type': 'exception'
            }
        }
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)

        self.assertTrue(isinstance(exception, FacebookPermissionException))
        self.assertEqual(10, exception.code)
        self.assertEqual(0, exception.sub_error_code)
        self.assertEqual('exception', exception.error_type)
        self.assertEqual('errmsg', exception.message)
        self.assertEqual(json_str, exception.raw_response)
        self.assertEqual(401, exception.status_code)

        params['error']['code'] = 200
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookPermissionException))
        self.assertEqual(200, exception.code)

        params['error']['code'] = 250
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookPermissionException))
        self.assertEqual(250, exception.code)

        params['error']['code'] = 299
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)
        self.assertTrue(isinstance(exception, FacebookPermissionException))
        self.assertEqual(299, exception.code)

    def test_client_exceptions(self):
        params = {
            'error': {
                'code': 506,
                'message': 'errmsg',
                'error_subcode': 0,
                'type': 'exception'
            }
        }
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 401)

        self.assertTrue(isinstance(exception, FacebookClientException))
        self.assertEqual(506, exception.code)
        self.assertEqual(0, exception.sub_error_code)
        self.assertEqual('exception', exception.error_type)
        self.assertEqual('errmsg', exception.message)
        self.assertEqual(json_str, exception.raw_response)
        self.assertEqual(401, exception.status_code)

    def test_other_exceptions(self):
        params = {
            'error': {
                'code': 42,
                'message': 'ship love',
                'error_subcode': 0,
                'type': 'feature'
            }
        }
        json_str = json.dumps(params)
        exception = FacebookRequestException.create(json_str, params, 200)

        self.assertTrue(isinstance(exception, FacebookOtherException))
        self.assertEqual(42, exception.code)
        self.assertEqual(0, exception.sub_error_code)
        self.assertEqual('feature', exception.error_type)
        self.assertEqual('ship love', exception.message)
        self.assertEqual(json_str, exception.raw_response)
        self.assertEqual(200, exception.status_code)

    def test_validate_throws_exception(self):
        bogus_session = FacebookSession('invalid-token')
        with self.assertRaises(FacebookSDKException):
            bogus_session.validate()

    def test_invalid_credentials_exception(self):
        bogus_session = FacebookSession('invalid-token')
        with self.assertRaises(FacebookAuthorizationException):
            bogus_session.validate('invalid-app-id', 'invalid-app-secret')
