# -*- coding: utf-8 -*-
import unittest

from facebook.session import FacebookSession
from tests.facebook_test_helper import FacebookTestHelper


class TestFacebookSession(unittest.TestCase):

    def test_session_token(self):
        session = FacebookSession(FacebookTestHelper.get_app_token())
        self.assertEqual(FacebookTestHelper.get_app_token(), session.get_token())
