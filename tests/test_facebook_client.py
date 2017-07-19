# -*- coding: utf-8 -*-
import os
import unittest

from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException
from python_facebook.sdk.facebook import Facebook
from python_facebook.sdk.facebook_app import FacebookApp
from python_facebook.sdk.facebook_client import FacebookClient
from python_facebook.sdk.graph_nodes.graph_node import GraphNode
from python_facebook.sdk.http_clients.facebook_requests_http_client import FacebookRequestsHttpClient
from python_facebook.sdk.request import FacebookRequest
from python_facebook.sdk.response import FacebookResponse
from tests.fixtures.my_foo_client_handler import MyFooClientHandler


class FacebookClientTest(unittest.TestCase):

    def setUp(self):
        self.fb_app = FacebookApp('id', 'shhhh!')
        self.fb_client = FacebookClient(MyFooClientHandler())

    def test_acustom_http_client_can_be_injected(self):
        handler = MyFooClientHandler()
        client = FacebookClient(handler)
        http_handler = client.get_http_client_handler()

        self.assertIsInstance(http_handler, MyFooClientHandler)

    def test_the_http_client_will_fallback_to_default(self):
        client = FacebookClient()
        http_handler = client.get_http_client_handler()

        self.assertIsInstance(http_handler, FacebookRequestsHttpClient)

    def test_beta_mode_can_be_disabled_or_enabled_via_constructor(self):
        client = FacebookClient(None, False)
        url = client.get_base_graph_url()
        self.assertEqual(FacebookClient.BASE_GRAPH_URL, url)

        client = FacebookClient(None, True)
        url = client.get_base_graph_url()
        self.assertEqual(FacebookClient.BASE_GRAPH_URL_BETA, url)

    def test_beta_mode_can_be_disabled_or_enabled_via_method(self):
        client = FacebookClient()
        client.enable_beta_mode(False)
        url = client.get_base_graph_url()
        self.assertEqual(FacebookClient.BASE_GRAPH_URL, url)

        client.enable_beta_mode(True)
        url = client.get_base_graph_url()
        self.assertEqual(FacebookClient.BASE_GRAPH_URL_BETA, url)

    def test_afacebook_request_entity_can_be_used_to_send_arequest_to_graph(self):
        fb_request = FacebookRequest(self.fb_app, 'token', 'GET', '/foo')
        response = self.fb_client.send_request(fb_request)

        self.assertIsInstance(response, FacebookResponse)
        self.assertEqual(200, response.get_http_status_code())
        self.assertEqual('{"data":[{"id":"123","name":"Foo"},{"id":"1337","name":"Bar"}]}',
                         response.get_body())

    def test_arequest_of_params_will_be_url_encoded(self):
        fb_request = FacebookRequest(self.fb_app, 'token', 'POST', '/foo', {'foo': 'bar'})
        response = self.fb_client.send_request(fb_request)

        headers_sent = response.get_request().get_headers()

        self.assertEqual('application/x-www-form-urlencoded', headers_sent['Content-Type'])

    def test_afacebook_request_validates_the_access_token_when_one_is_not_provided(self):
        request = FacebookRequest(self.fb_app, None, 'GET', '/foo')
        with self.assertRaises(FacebookSDKException):
            self.fb_client.send_request(request)

    def test_can_create_atest_user_and_get_the_profile_and_then_delete_the_test_user(self):
        app = self._initialize_test_app()
        client = FacebookClient()

        # Create a test user
        test_user_path = '/' + app.get_id() + '/accounts/test-users'

        params = {
            'installed': True,
            'name': 'Foo Pythonunit User',
            'locale': 'en_US',
            'permissions': ','.join(['read_stream', 'user_photos'])
        }

        request = FacebookRequest(
            app,
            app.get_access_token(),
            'POST',
            test_user_path,
            params
        )
        response = client.send_request(request).get_graph_node()
        test_user_id = response.get_field('id')
        test_user_access_token = response.get_field('access_token')

        # Get the test user's profile
        request = FacebookRequest(
            app,
            test_user_access_token,
            'GET',
            '/me',
        )
        graph_node = client.send_request(request).get_graph_node()

        self.assertIsInstance(graph_node, GraphNode)
        self.assertIsNotNone(graph_node.get_field('id'))
        self.assertIsNotNone('Foo Pythonunit User', graph_node.get_field('name'))

        # delete user
        request = FacebookRequest(
            app,
            app.get_access_token(),
            'DELETE',
            '/' + str(test_user_id),
        )
        graph_node = client.send_request(request).get_graph_node()

        self.assertTrue(graph_node.get_field('success'))

    def _initialize_test_app(self):
        app_id = os.environ.get(Facebook.APP_ID_ENV_NAME)
        app_secret = os.environ.get(Facebook.APP_SECRET_ENV_NAME)

        if not app_id or not app_secret:
            raise FacebookSDKException('You must specify your app_id/app_secret pair as environment variables')

        return FacebookApp(app_id, app_secret)
