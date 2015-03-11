# -*- coding: utf-8 -*-
import unittest

from python_facebook.request import FacebookRequest
from tests.facebook_test_helper import FacebookTestHelper


class TestFacebookRequest(unittest.TestCase):

    def setUp(self):
        super(TestFacebookRequest, self).setUp()
        FacebookTestHelper.initialize()

    def tearDown(self):
        super(TestFacebookRequest, self).tearDown()
        FacebookTestHelper.delete_test_user()

    def test_gets_the_logged_in_users_profile(self):
        response = FacebookRequest(
            FacebookTestHelper.test_session(),
            'GET',
            '/me'
        ).execute().get_graph_object()
        self.assertIsNotNone(response.id)
        self.assertIsNotNone(response.name)
