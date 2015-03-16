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
