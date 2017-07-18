# -*- coding: utf-8 -*-
import unittest

from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException
from python_facebook.sdk.facebook import Facebook
from python_facebook.sdk.facebook_app import FacebookApp
from python_facebook.sdk.file_upload.facebook_file import FacebookFile
from python_facebook.sdk.request import FacebookRequest
from python_facebook.sdk.session import FacebookSession
from tests.facebook_test_credentials import FacebookTestCredentials
from tests.facebook_test_helper import FacebookTestHelper


class TestFacebookRequest(unittest.TestCase):
    
    def testAnEmptyRequestEntityCanInstantiate(self):
        app = FacebookApp('123', 'foo_secret')
        request = FacebookRequest(app)
        self.assertIsInstance(request, FacebookRequest)

    def testAMissingAccessTokenWillThrow(self):
        app = FacebookApp('123', 'foo_secret')
        request = FacebookRequest(app)
        with self.assertRaises(FacebookSDKException):
            request.validate_access_token()

    def testAMissingMethodWillThrow(self):
        app = FacebookApp('123', 'foo_secret')
        request = FacebookRequest(app)
        with self.assertRaises(FacebookSDKException):
            request.validate_method()

    def testAnInvalidMethodWillThrow(self):
        app = FacebookApp('123', 'foo_secret')
        request = FacebookRequest(app, 'foo_token', 'FOO')
        with self.assertRaises(FacebookSDKException):
            request.validate_method()

    def testGetHeadersWillAutoAppendETag(self):
        app = FacebookApp('123', 'foo_secret')
        request = FacebookRequest(app, None, 'GET', '/foo', [], 'fooETag')
        headers = request.get_headers()
        expectedHeaders = FacebookRequest.get_default_headers()
        expectedHeaders['If-None-Match'] = 'fooETag';
        self.assertEqual(expectedHeaders, headers)

    def testGetParamsWillAutoAppendAccessTokenAndAppSecretProof(self):
        app = FacebookApp('123', 'foo_secret')
        request = FacebookRequest(app, 'foo_token', 'POST', '/foo', {'foo': 'bar'})
        params = request.get_params()
        self.assertEqual({
            'foo': 'bar',
            'access_token': 'foo_token',
            'appsecret_proof': 'df4256903ba4e23636cc142117aa632133d75c642bd2a68955be1443bd14deb9',
        }, params)

    def testAnAccessTokenCanBeSetFromTheParams(self):
        app = FacebookApp('123', 'foo_secret')
        request = FacebookRequest(app, None, 'POST', '/me', {'access_token': 'bar_token'})
        accessToken = request.get_access_token()
        self.assertEqual('bar_token', accessToken)

    def testAccessTokenConflictsWillThrow(self):
        app = FacebookApp('123', 'foo_secret')
        with self.assertRaises(FacebookSDKException):
            FacebookRequest(app, 'foo_token', 'POST', '/me', {'access_token': 'bar_token'})

    def testAProperUrlWillBeGenerated(self):
        app = FacebookApp('123', 'foo_secret')
        getRequest = FacebookRequest(app, 'foo_token', 'GET', '/foo', {'foo': 'bar'})

        getUrl = getRequest.get_url()
        expectedParams = 'access_token=foo_token&appsecret_proof=df4256903ba4e23636cc142117aa632133d75c642bd2a68955be1443bd14deb9&foo=bar'
        expectedUrl = '/{}/foo?{}'.format(Facebook.DEFAULT_GRAPH_VERSION, expectedParams)
        self.assertEqual(expectedUrl, getUrl)

        postRequest = FacebookRequest(app, 'foo_token', 'POST', '/bar', {'foo': 'bar'})
        postUrl = postRequest.get_url()
        expectedUrl = '/{}/bar'.format(Facebook.DEFAULT_GRAPH_VERSION)
        self.assertEqual(expectedUrl, postUrl)

    def testAuthenticationParamsAreStrippedAndReapplied(self):
        app = FacebookApp('123', 'foo_secret')
        request = FacebookRequest(
            app, access_token='foo_token', method='GET', endpoint='/foo',
            params={'access_token': 'foo_token', 'appsecret_proof': 'bar_app_secret', 'bar': 'baz'})
        url = request.get_url()
        expectedParams = 'access_token=foo_token&appsecret_proof=df4256903ba4e23636cc142117aa632133d75c642bd2a68955be1443bd14deb9&bar=baz'
        expectedUrl = '/{}/foo?{}'.format(Facebook.DEFAULT_GRAPH_VERSION, expectedParams)
        self.assertEqual(expectedUrl, url)
        params = request.get_params()
        expectedParams = {
            'access_token': 'foo_token',
            'appsecret_proof': 'df4256903ba4e23636cc142117aa632133d75c642bd2a68955be1443bd14deb9',
            'bar': 'baz',
        }
        self.assertEqual(expectedParams, params)

    # def testAFileCanBeAddedToParams(self):
    #     myFile = FacebookFile(__DIR__.'/foo.txt')
    #     params = {
    #         'name': 'Foo Bar',
    #         'source': myFile,
    #     }
    #     app = FacebookApp('123', 'foo_secret')
    #     request = FacebookRequest(app, 'foo_token', 'POST', '/foo/photos', params)
    #     actualParams = request.get_params()
    #     self.assertTrue(request.contains_file_uploads())
    #     self.assertFalse(request.contains_video_uploads())
    #     self.assertTrue('source' not in actualParams))
    #     self.assertEqual('Foo Bar', actualParams['name'])
    #
    # def testAVideoCanBeAddedToParams(self):
    #     myFile = FacebookVideo(__DIR__.'/foo.txt')
    #     params = {
    #         'name': 'Foo Bar',
    #         'source': myFile,
    #     }
    #     app = FacebookApp('123', 'foo_secret')
    #     request = FacebookRequest(app, 'foo_token', 'POST', '/foo/videos', params)
    #     actualParams = request.get_params()
    #     self.assertTrue(request.contains_file_uploads())
    #     self.assertTrue(request.contains_video_uploads())
    #     self.assertTrue('source' not in actualParams))
    #     self.assertEqual('Foo Bar', actualParams['name'])
