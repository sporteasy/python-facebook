# -*- coding: utf-8 -*-
import unittest
import json

from python_facebook.sdk.exceptions.facebook_authentication_exception import FacebookAuthenticationException
from python_facebook.sdk.exceptions.facebook_authorization_exception import FacebookAuthorizationException
from python_facebook.sdk.exceptions.facebook_client_exception import FacebookClientException
from python_facebook.sdk.exceptions.facebook_resumable_upload_exception import FacebookResumableUploadException
from python_facebook.sdk.exceptions.facebook_other_exception import FacebookOtherException
from python_facebook.sdk.exceptions.facebook_server_exception import FacebookServerException
from python_facebook.sdk.exceptions.facebook_throttle_exception import FacebookThrottleException
from python_facebook.sdk.exceptions.facebook_response_exception import FacebookResponseException
from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException
from python_facebook.sdk.session import FacebookSession


class MockResponse(object):
    def __init__(self, json_str):
        self.body = json_str

    def get_decoded_body(self):
        return json.loads(self.body)


class TestFacebookResponseException(unittest.TestCase):

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
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)

        self.assertTrue(isinstance(exception, FacebookAuthenticationException))
        self.assertEqual(100, exception.code)
        self.assertEqual('errmsg', exception.message)

        params['error']['code'] = 102
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
        self.assertTrue(isinstance(exception, FacebookAuthenticationException))
        self.assertEqual(102, exception.code)

        params['error']['code'] = 190
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
        self.assertTrue(isinstance(exception, FacebookAuthenticationException))
        self.assertEqual(190, exception.code)

        params['error']['type'] = 'OAuthException'
        params['error']['code'] = 0
        params['error']['error_subcode'] = 458
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
        self.assertTrue(isinstance(exception, FacebookAuthenticationException))

        params['error']['error_subcode'] = 460
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
        self.assertTrue(isinstance(exception, FacebookAuthenticationException))

        params['error']['error_subcode'] = 463
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
        self.assertTrue(isinstance(exception, FacebookAuthenticationException))

        params['error']['error_subcode'] = 467
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
        self.assertTrue(isinstance(exception, FacebookAuthenticationException))

        params['error']['error_subcode'] = 0
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
        self.assertTrue(isinstance(exception, FacebookAuthenticationException))

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
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)

        self.assertTrue(isinstance(exception, FacebookServerException))
        self.assertEqual(1, exception.code)
        self.assertEqual('errmsg', exception.message)

        params['error']['code'] = 2
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
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
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)

        self.assertTrue(isinstance(exception, FacebookThrottleException))
        self.assertEqual(4, exception.code)
        self.assertEqual('errmsg', exception.message)

        params['error']['code'] = 17
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
        self.assertTrue(isinstance(exception, FacebookThrottleException))
        self.assertEqual(17, exception.code)

        params['error']['code'] = 341
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
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
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)

        self.assertTrue(isinstance(exception, FacebookAuthenticationException))
        self.assertEqual(230, exception.code)
        self.assertEqual('errmsg', exception.message)

        params['error']['code'] = 464
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
        self.assertTrue(isinstance(exception, FacebookAuthenticationException))
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
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)

        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
        self.assertEqual(10, exception.code)
        self.assertEqual('errmsg', exception.message)

        params['error']['code'] = 200
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
        self.assertEqual(200, exception.code)

        params['error']['code'] = 250
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
        self.assertEqual(250, exception.code)

        params['error']['code'] = 299
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)
        self.assertTrue(isinstance(exception, FacebookAuthorizationException))
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
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)

        self.assertTrue(isinstance(exception, FacebookClientException))
        self.assertEqual(506, exception.code)
        self.assertEqual('errmsg', exception.message)

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
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)

        self.assertTrue(isinstance(exception, FacebookOtherException))
        self.assertEqual(42, exception.code)
        self.assertEqual('ship love', exception.message)

    def test_validate_throws_exception(self):
        bogus_session = FacebookSession('invalid-token')
        with self.assertRaises(FacebookSDKException):
            bogus_session.validate()

    def test_invalid_credentials_exception(self):
        bogus_session = FacebookSession('invalid-token')
        with self.assertRaises(FacebookAuthorizationException):
            bogus_session.validate('invalid-app-id', 'invalid-app-secret')

    def test_upload_exception(self):
        params = {
            'error': {
                'code': 400,
                'message': 'upload error',
                'error_subcode': 1363030,
                'type': 'error'
            }
        }
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)

        self.assertTrue(isinstance(exception, FacebookResumableUploadException))
        self.assertEqual(400, exception.code)
        self.assertEqual('upload error', exception.message)

        params['error']['error_subcode'] = 1363019
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)

        self.assertTrue(isinstance(exception, FacebookResumableUploadException))
        self.assertEqual(400, exception.code)
        self.assertEqual('upload error', exception.message)

        params['error']['error_subcode'] = 1363037
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)

        self.assertTrue(isinstance(exception, FacebookResumableUploadException))
        self.assertEqual(400, exception.code)
        self.assertEqual('upload error', exception.message)

        params['error']['error_subcode'] = 1363033
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)

        self.assertTrue(isinstance(exception, FacebookResumableUploadException))
        self.assertEqual(400, exception.code)
        self.assertEqual('upload error', exception.message)

        params['error']['error_subcode'] = 1363021
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)

        self.assertTrue(isinstance(exception, FacebookResumableUploadException))
        self.assertEqual(400, exception.code)
        self.assertEqual('upload error', exception.message)

        params['error']['error_subcode'] = 1363041
        json_str = json.dumps(params)
        response = MockResponse(json_str)
        exception = FacebookResponseException.create(response)

        self.assertTrue(isinstance(exception, FacebookResumableUploadException))
        self.assertEqual(400, exception.code)
        self.assertEqual('upload error', exception.message)
