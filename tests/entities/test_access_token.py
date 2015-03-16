# -*- coding: utf-8 -*-
import unittest
import time

# from python_facebook.sdk.entities.access_token import AccessToken
from python_facebook.sdk.entities.access_token import AccessToken


class TestAccessToken(unittest.TestCase):

    def test_an_access_token_can_be_returned_as_a_string(self):
        access_token = AccessToken('foo_token')

        self.assertEqual('foo_token', str(access_token))

    def test_short_lived_access_tokens_can_be_detected(self):
        an_hour_and_a_half = time.time() + (1.5 * 60)
        access_token = AccessToken('foo_token', an_hour_and_a_half)

        is_long_lived = access_token.is_long_lived()

        self.assertFalse(is_long_lived, 'Expected access token to be short lived.')

    def test_long_lived_access_tokens_can_be_detected(self):
        a_week = time.time() + (60 * 60 * 24 * 7)
        access_token = AccessToken('foo_token', a_week)

        is_long_lived = access_token.is_long_lived()

        self.assertTrue(is_long_lived, 'Expected access token to be long lived.')
