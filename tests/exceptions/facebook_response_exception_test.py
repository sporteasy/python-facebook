# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import json

from python_facebook.sdk.exceptions.facebook_authentication_exception import FacebookAuthenticationException
from python_facebook.sdk.exceptions.facebook_authorization_exception import FacebookAuthorizationException
from python_facebook.sdk.exceptions.facebook_client_exception import FacebookClientException
from python_facebook.sdk.exceptions.facebook_other_exception import FacebookOtherException
from python_facebook.sdk.exceptions.facebook_server_exception import FacebookServerException
from python_facebook.sdk.exceptions.facebook_throttle_exception import FacebookThrottleException
from python_facebook.sdk.facebook_app import FacebookApp
from python_facebook.sdk.response import FacebookResponse

from python_facebook.sdk.exceptions.facebook_response_exception import FacebookResponseException
from python_facebook.sdk.request import FacebookRequest


class FacebookResponseExceptionTest(unittest.TestCase):

    def setUp(self):
        self.request = FacebookRequest(FacebookApp('123', 'foo'))

    def testAuthenticationExceptions(self):
        params = {
            'error': {
                'code': 100,
                'message': 'errmsg',
                'error_subcode': 0,
                'type': 'exception'
            },
        }
        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthenticationException)
        self.assertEqual(100, exception.code)
        self.assertEqual(0, exception.get_sub_error_code())
        self.assertEqual('exception', exception.get_error_type())
        self.assertEqual('errmsg', exception.message)
        self.assertEqual(json.dumps(params), exception.get_raw_response())
        self.assertEqual(401, exception.get_http_status_code())
        params['error']['code'] = 102

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthenticationException)
        self.assertEqual(102, exception.code)
        params['error']['code'] = 190

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthenticationException)
        self.assertEqual(190, exception.code)
        params['error']['type'] = 'OAuthException'
        params['error']['code'] = 0
        params['error']['error_subcode'] = 458

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthenticationException)
        self.assertEqual(458, exception.get_sub_error_code())
        params['error']['error_subcode'] = 460

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthenticationException)
        self.assertEqual(460, exception.get_sub_error_code())
        params['error']['error_subcode'] = 463

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthenticationException)
        self.assertEqual(463, exception.get_sub_error_code())
        params['error']['error_subcode'] = 467

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthenticationException)
        self.assertEqual(467, exception.get_sub_error_code())
        params['error']['error_subcode'] = 0

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthenticationException)
        self.assertEqual(0, exception.get_sub_error_code())

    def testServerExceptions(self):
        params = {
            'error': {
                'code': 1,
                'message': 'errmsg',
                'error_subcode': 0,
                'type': 'exception'
            },
        }

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=500)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookServerException)
        self.assertEqual(1, exception.code)
        self.assertEqual(0, exception.get_sub_error_code())
        self.assertEqual('exception', exception.get_error_type())
        self.assertEqual('errmsg', exception.message)
        self.assertEqual(json.dumps(params), exception.get_raw_response())
        self.assertEqual(500, exception.get_http_status_code())
        params['error']['code'] = 2

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=500)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookServerException)
        self.assertEqual(2, exception.code)

    def testThrottleExceptions(self):
        params = {
            'error': {
                'code': 4,
                'message': 'errmsg',
                'error_subcode': 0,
                'type': 'exception'
            },
        }

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookThrottleException)
        self.assertEqual(4, exception.code)
        self.assertEqual(0, exception.get_sub_error_code())
        self.assertEqual('exception', exception.get_error_type())
        self.assertEqual('errmsg', exception.message)
        self.assertEqual(json.dumps(params), exception.get_raw_response())
        self.assertEqual(401, exception.get_http_status_code())
        params['error']['code'] = 17

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookThrottleException)
        self.assertEqual(17, exception.code)
        params['error']['code'] = 341

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookThrottleException)
        self.assertEqual(341, exception.code)

    def testUserIssueExceptions(self):
        params = {
            'error': {
                'code': 230,
                'message': 'errmsg',
                'error_subcode': 459,
                'type': 'exception'
            },
        }

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthenticationException)
        self.assertEqual(230, exception.code)
        self.assertEqual(459, exception.get_sub_error_code())
        self.assertEqual('exception', exception.get_error_type())
        self.assertEqual('errmsg', exception.message)
        self.assertEqual(json.dumps(params), exception.get_raw_response())
        self.assertEqual(401, exception.get_http_status_code())
        params['error']['error_subcode'] = 464

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthenticationException)
        self.assertEqual(464, exception.get_sub_error_code())

    def testAuthorizationExceptions(self):
        params = {
            'error': {
                'code': 10,
                'message': 'errmsg',
                'error_subcode': 0,
                'type': 'exception'
            },
        }

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthorizationException)
        self.assertEqual(10, exception.code)
        self.assertEqual(0, exception.get_sub_error_code())
        self.assertEqual('exception', exception.get_error_type())
        self.assertEqual('errmsg', exception.message)
        self.assertEqual(json.dumps(params), exception.get_raw_response())
        self.assertEqual(401, exception.get_http_status_code())
        params['error']['code'] = 200

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthorizationException)
        self.assertEqual(200, exception.code)
        params['error']['code'] = 250

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthorizationException)
        self.assertEqual(250, exception.code)
        params['error']['code'] = 299

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookAuthorizationException)
        self.assertEqual(299, exception.code)

    def testClientExceptions(self):
        params = {
            'error': {
                'code': 506,
                'message': 'errmsg',
                'error_subcode': 0,
                'type': 'exception'
            },
        }

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=401)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookClientException)
        self.assertEqual(506, exception.code)
        self.assertEqual(0, exception.get_sub_error_code())
        self.assertEqual('exception', exception.get_error_type())
        self.assertEqual('errmsg', exception.message)
        self.assertEqual(json.dumps(params), exception.get_raw_response())
        self.assertEqual(401, exception.get_http_status_code())

    def testOtherException(self):
        params = {
            'error': {
                'code': 42,
                'message': 'ship love',
                'error_subcode': 0,
                'type': 'feature'
            },
        }

        response = FacebookResponse(self.request, json.dumps(params), http_status_code=200)
        exception = FacebookResponseException.create(response)
        self.assertIsInstance(exception.get_previous(), FacebookOtherException)
        self.assertEqual(42, exception.code)
        self.assertEqual(0, exception.get_sub_error_code())
        self.assertEqual('feature', exception.get_error_type())
        self.assertEqual('ship love', exception.message)
        self.assertEqual(json.dumps(params), exception.get_raw_response())
        self.assertEqual(200, exception.get_http_status_code())
