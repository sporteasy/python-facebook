# -*- coding: utf-8 -*-
from python_facebook.sdk.exceptions import FacebookSDKException
from python_facebook.sdk.request import FacebookRequest
from python_facebook.sdk.session import FacebookSession
from tests.facebook_test_credentials import FacebookTestCredentials


class FacebookTestHelper(object):

    _TEST_SESSION = None

    TEST_USER_PERMISSIONS = ['read_stream', 'user_photos']

    test_user_access_token = None
    test_user_id = None

    @classmethod
    def initialize(cls):
        if not FacebookTestCredentials.APP_ID or not FacebookTestCredentials.APP_SECRET:
            raise FacebookSDKException('You must fill out Facebook test credentials')

        if not isinstance(cls._TEST_SESSION, FacebookSession):
            cls._TEST_SESSION = cls.create_test_session()

    @classmethod
    def create_test_session(cls):
        cls.create_test_user_and_get_access_token()
        return FacebookSession(cls.test_user_access_token)

    @classmethod
    def create_test_user_and_get_access_token(cls):
        test_user_path = '/' + FacebookTestCredentials.APP_ID + '/accounts/test-users'
        params = {
            'installed': True,
            'name': 'Foo Python User',
            'locale': 'en_US',
            'permissions': ','.join(cls.TEST_USER_PERMISSIONS)
        }
        request = FacebookRequest(
            FacebookTestCredentials.APP_ID,
            FacebookTestCredentials.APP_SECRET,
            cls.get_app_session(),
            'POST',
            test_user_path,
            params
        )
        response = request.execute().get_graph_object()
        cls.test_user_id = response.id
        cls.test_user_access_token = response.access_token

    @classmethod
    def delete_test_user(cls):
        if not cls.test_user_id:
            return

        test_user_path = '/' + cls.test_user_id
        request = FacebookRequest(
            FacebookTestCredentials.APP_ID,
            FacebookTestCredentials.APP_SECRET,
            cls.get_app_session(),
            'DELETE',
            test_user_path
        )
        request.execute()

    @classmethod
    def get_app_session(cls):
        return FacebookSession(cls.get_app_token())

    @classmethod
    def get_app_token(cls):
        return FacebookTestCredentials.APP_ID + '|' + FacebookTestCredentials.APP_SECRET

    @classmethod
    def test_session(cls):
        return cls._TEST_SESSION
