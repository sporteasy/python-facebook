# -*- coding: utf-8 -*-
import unittest

from python_facebook.sdk.request import FacebookRequest
from python_facebook.sdk.session import FacebookSession
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

    def test_can_post_and_delete(self):
        # Create a test user
        params = {
            'name': 'Foo User'
        }
        response = FacebookRequest(
            FacebookTestCredentials.APP_ID,
            FacebookTestCredentials.APP_SECRET,
            FacebookSession(FacebookTestHelper.get_app_token()),
            'POST',
            '/' + FacebookTestCredentials.APP_ID + '/accounts/test-users',
            params
        ).execute().get_graph_object()
        user_id = response.id

        # Delete test user
        response = FacebookRequest(
            FacebookTestCredentials.APP_ID,
            FacebookTestCredentials.APP_SECRET,
            FacebookSession(FacebookTestHelper.get_app_token()),
            'DELETE',
            '/' + user_id,
            params
        ).execute().get_graph_object()
        self.assertEqual(response.success, True)

    def test_etag_hit(self):
        response = FacebookRequest(
            FacebookTestCredentials.APP_ID,
            FacebookTestCredentials.APP_SECRET,
            FacebookTestHelper.test_session(),
            'GET',
            '/104048449631599'
        ).execute()

        self.assertFalse(response.etag_hit)

        response = FacebookRequest(
            FacebookTestCredentials.APP_ID,
            FacebookTestCredentials.APP_SECRET,
            FacebookTestHelper.test_session(),
            'GET',
            '/104048449631599',
            None,
            None,
            response.etag
        ).execute()

        self.assertTrue(response.etag_hit)
        self.assertIsNone(response.etag)

    def test_etag_miss(self):
        response = FacebookRequest(
            FacebookTestCredentials.APP_ID,
            FacebookTestCredentials.APP_SECRET,
            FacebookTestHelper.test_session(),
            'GET',
            '/104048449631599',
            None,
            None,
            'someRandomValue'
        ).execute()

        self.assertFalse(response.etag_hit)
        self.assertIsNotNone(response.etag)

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

    def test_app_secret_proof(self):
        enable_app_secret_proof = FacebookSession.use_app_secret_proof()

        FacebookSession.enable_app_secret_proof(True)
        request = FacebookRequest(
            FacebookTestCredentials.APP_ID,
            FacebookTestCredentials.APP_SECRET,
            FacebookTestHelper.test_session(),
            'GET',
            '/me'
        )
        self.assertTrue('appsecret_proof' in request.get_parameters())

        FacebookSession.enable_app_secret_proof(False)
        request = FacebookRequest(
            FacebookTestCredentials.APP_ID,
            FacebookTestCredentials.APP_SECRET,
            FacebookTestHelper.test_session(),
            'GET',
            '/me'
        )
        self.assertFalse('appsecret_proof' in request.get_parameters())

        FacebookSession.enable_app_secret_proof(enable_app_secret_proof)
