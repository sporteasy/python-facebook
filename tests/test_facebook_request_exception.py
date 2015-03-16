# -*- coding: utf-8 -*-
import unittest
import json

from python_facebook.sdk.exceptions import (
    FacebookRequestException,
    FacebookAuthorizationException
)


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
        self.assertEqual(401, exception.status_code)
