# -*- coding: utf-8 -*-
import os
import unittest

from python_facebook.sdk.authentication.access_token import AccessToken
from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException
from python_facebook.sdk.facebook import Facebook
from python_facebook.sdk.facebook_client import FacebookClient
from python_facebook.sdk.url.facebook_url_detection_handler import FacebookUrlDetectionHandler
from tests.fixtures.foo_bar_pseudo_random_string_generator import FooBarPseudoRandomStringGenerator
from tests.fixtures.foo_client_interface import FooClientInterface
from tests.fixtures.foo_persistent_data_interface import FooPersistentDataInterface
from tests.fixtures.foo_url_detection_interface import FooUrlDetectionInterface


class FacebookTestCase(unittest.TestCase):

    config = {
        'app_id': '1337',
        'app_secret': 'foo_secret'
    }

    def test_instantiating_without_app_id_raises(self):
        # unset value so there is no fallback to test expected Exception
        value = os.environ.get(Facebook.APP_ID_ENV_NAME)
        os.environ[Facebook.APP_ID_ENV_NAME] = ""
        config = {
            'app_secret': 'foo_secret'
        }
        with self.assertRaises(FacebookSDKException):
            Facebook(config)
        os.environ[Facebook.APP_ID_ENV_NAME] = value

    def test_instantiating_without_app_secret_raises(self):
        # unset value so there is no fallback to test expected Exception
        value = os.environ.get(Facebook.APP_SECRET_ENV_NAME)
        os.environ[Facebook.APP_SECRET_ENV_NAME] = ""
        config = {
            'app_id': 'foo_id'
        }
        with self.assertRaises(FacebookSDKException):
            Facebook(config)
        os.environ[Facebook.APP_SECRET_ENV_NAME] = value

    def test_the_url_handler_will_default_to_the_facebook_implementation(self):
        fb = Facebook(self.config)
        self.assertIsInstance(fb.get_url_detection_handler(), FacebookUrlDetectionHandler)

    def test_an_access_token_can_be_set_as_astring(self):
        fb = Facebook(self.config)
        fb.set_default_access_token('foo_token')
        access_token = fb.get_default_access_token()

        self.assertIsInstance(access_token, AccessToken)
        self.assertEqual('foo_token', str(access_token))

    def test_an_access_token_can_be_set_as_an_access_token_entity(self):
        fb = Facebook(self.config)
        fb.set_default_access_token(AccessToken('bar_token'))
        access_token = fb.get_default_access_token()

        self.assertIsInstance(access_token, AccessToken)
        self.assertEqual('bar_token', str(access_token))

    def test_setting_an_access_that_is_not_string_or_access_token_throws(self):
        config = self.config.copy()
        config.update({'default_access_token': 123})
        with self.assertRaises(ValueError):
            fb = Facebook(config)

    def test_creating_anew_request_will_default_to_the_proper_config(self):
        config = self.config.copy()
        config.update({
            'default_access_token': 'foo_token',
            'enable_beta_mode': True,
            'default_graph_version': 'v1337'
        })

        fb = Facebook(config)
        request = fb.request('FOO_VERB', '/foo')
        self.assertEqual('1337', request.get_app().get_id())
        self.assertEqual('foo_secret', request.get_app().get_secret())
        self.assertEqual('foo_token', str(request.get_access_token()))
        self.assertEqual('v1337', str(request.get_graph_version()))
        self.assertEqual(FacebookClient.BASE_GRAPH_URL_BETA,
                         fb.get_client().get_base_graph_url())

    def test_can_inject_custom_handlers(self):
        config = self.config.copy()
        config.update({
            'http_client_handler': FooClientInterface(),
            'persistent_data_handler': FooPersistentDataInterface(),
            'url_detection_handler': FooUrlDetectionInterface(),
            'pseudo_random_string_generator': FooBarPseudoRandomStringGenerator()
        })

        fb = Facebook(config)

        self.assertIsInstance(fb.get_client().get_http_client_handler(),
                              FooClientInterface)
        self.assertIsInstance(fb.get_redirect_login_helper().get_persistent_data_handler(),
                              FooPersistentDataInterface)
        self.assertIsInstance(fb.get_redirect_login_helper().get_url_detection_handler(),
                              FooUrlDetectionInterface)
        self.assertIsInstance(fb.get_redirect_login_helper().get_pseudo_random_string_generator(),
                              FooBarPseudoRandomStringGenerator)
