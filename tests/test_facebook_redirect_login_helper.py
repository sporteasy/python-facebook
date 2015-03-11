# -*- coding: utf-8 -*-
import unittest
import urllib

from facebook.helpers.login import FacebookRedirectLoginHelper
from facebook.request import FacebookRequest
from tests.facebook_test_credentials import FacebookTestCredentials


class TestFacebookRedirectLoginHelper(unittest.TestCase):

    REDIRECT_URL = 'http://invalid.zzz'

    def test_login_url(self):
        helper = FacebookRedirectLoginHelper(
            self.REDIRECT_URL,
            FacebookTestCredentials.APP_ID,
            FacebookTestCredentials.APP_SECRET
        )
        helper.disable_session_status_check()

        login_url = helper.get_login_url()
        params = {
            'client_id': FacebookTestCredentials.APP_ID,
            'redirect_uri': self.REDIRECT_URL,
            'state': helper.state,
            'scope': ','.join([])
        }

        expected_url = 'https://www.facebook.com/' + FacebookRequest.GRAPH_API_VERSION \
                       + '/dialog/oauth?'
        self.assertTrue(login_url.startswith(expected_url),
                        'Unexpected base login URL returned from getLoginUrl().')
        for key, val in params.items():
            self.assertIn(key + '=' + urllib.quote_plus(val), login_url)
