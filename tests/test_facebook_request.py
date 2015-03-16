# -*- coding: utf-8 -*-
import unittest

from python_facebook.sdk.request import FacebookRequest
from tests.facebook_test_credentials import FacebookTestCredentials
from tests.facebook_test_helper import FacebookTestHelper


class TestFacebookRequest(unittest.TestCase):

    def test_gets_the_logged_in_users_profile(self):
        response = FacebookRequest(
            FacebookTestCredentials.APP_ID,
            FacebookTestCredentials.APP_SECRET,
            FacebookTestHelper.test_session(),
            'GET',
            '/me'
        ).execute().get_graph_object()
        self.assertIsNotNone(response.id)
        self.assertIsNotNone(response.name)

    def test_gracefully_handles_url_appending(self):
        params = {}
        url = 'https://www.foo.com/'
        processed_url = FacebookRequest.append_params_to_url(url, params)
        self.assertEqual(url, processed_url)

        params = {
            'access_token': 'foo'
        }
        url = 'https://www.foo.com/'
        processed_url = FacebookRequest.append_params_to_url(url, params)
        self.assertEqual('https://www.foo.com/?access_token=foo', processed_url)

        params = {
            'access_token': 'foo',
            'bar': 'baz'
        }
        url = 'https://www.foo.com/?foo=bar'
        processed_url = FacebookRequest.append_params_to_url(url, params)
        self.assertEqual(
            'https://www.foo.com/?access_token=foo&bar=baz&foo=bar',
            processed_url
        )

        params = {
            'access_token': 'foo',
        }
        url = 'https://www.foo.com/?foo=bar&access_token=bar'
        processed_url = FacebookRequest.append_params_to_url(url, params)
        self.assertEqual(
            'https://www.foo.com/?access_token=bar&foo=bar',
            processed_url
        )
