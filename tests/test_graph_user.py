# -*- coding: utf-8 -*-
import unittest

from python_facebook.sdk.graph_user import GraphUser
from python_facebook.sdk.request import FacebookRequest
from tests.facebook_test_credentials import FacebookTestCredentials
from tests.facebook_test_helper import FacebookTestHelper


class TestGraphUser(unittest.TestCase):

    def test_me_returns_graph_user(self):
        response = FacebookRequest(
            FacebookTestCredentials.APP_ID,
            FacebookTestCredentials.APP_SECRET,
            FacebookTestHelper.test_session(),
            'GET',
            '/me'
        ).execute().get_graph_object(GraphUser)

        self.assertTrue(isinstance(response, GraphUser))
        session = FacebookTestHelper.test_session().get_session_info(
            FacebookTestCredentials.APP_ID,
            FacebookTestCredentials.APP_SECRET
        )
        self.assertEqual(response.id, session.user_id)
        self.assertIsNotNone(response.name)
        self.assertIsNotNone(response.last_name)
        self.assertIsNotNone(response.link)
