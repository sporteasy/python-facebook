# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest_data_provider import data_provider

from tests import PythonFacebookTestCase
from python_facebook.sdk.url.facebook_url_manipulator import FacebookUrlManipulator


class TestFacebookUrlManipulator(PythonFacebookTestCase):

    dirty_urls = lambda: (
        ('http://localhost/something?state=0000&foo=bar&code=abcd', 'http://localhost/something?foo=bar'),
        ('https://localhost/something?state=0000&foo=bar&code=abcd', 'https://localhost/something?foo=bar'),
        ('http://localhost/something?state=0000&foo=bar&error=abcd&error_reason=abcd&error_description=abcd'
         '&error_code=1', 'http://localhost/something?foo=bar'),
        ('https://localhost/something?state=0000&foo=bar&error=abcd&error_reason=abcd&error_description=abcd'
         '&error_code=1', 'https://localhost/something?foo=bar'),
        ('http://localhost/something?state=0000&foo=bar&error=abcd', 'http://localhost/something?foo=bar'),
        ('https://localhost/something?state=0000&foo=bar&error=abcd', 'https://localhost/something?foo=bar'),
        ('https://localhost:1337/something?state=0000&foo=bar&error=abcd', 'https://localhost:1337/something?foo=bar'),
        ('https://localhost:1337/something?state=0000&code=foo', 'https://localhost:1337/something'),
        ('https://localhost/something/?state=0000&code=foo&foo=bar', 'https://localhost/something/?foo=bar'),
        ('https://localhost/something/?state=0000&code=foo', 'https://localhost/something/'),
    )

    @data_provider(dirty_urls)
    def test_params_get_removed_from_a_url(self, dirty_url, expected_clean_url):
        remove_params = [
            'state',
            'code',
            'error',
            'error_reason',
            'error_description',
            'error_code',
        ]
        current_uri = FacebookUrlManipulator.remove_params_from_url(dirty_url, remove_params)
        self.assertEqual(expected_clean_url, current_uri)

    def test_gracefully_handles_url_appending(self):
        params = {}
        url = 'https://www.foo.com/'
        processed_url = FacebookUrlManipulator.append_params_to_url(url, params)
        self.assertEqual('https://www.foo.com/', processed_url)

        params = {'access_token': 'foo'}
        url = 'https://www.foo.com/'
        processed_url = FacebookUrlManipulator.append_params_to_url(url, params)
        self.assertEqual('https://www.foo.com/?access_token=foo', processed_url)

        params = {
            'access_token': 'foo',
            'bar': 'baz'
        }
        url = 'https://www.foo.com/?foo=bar'
        processed_url = FacebookUrlManipulator.append_params_to_url(url, params)
        self.assertEqual('https://www.foo.com/?access_token=foo&bar=baz&foo=bar', processed_url)

        params = {
            'access_token': 'foo',
        }
        url = 'https://www.foo.com/?foo=bar&access_token=bar'
        processed_url = FacebookUrlManipulator.append_params_to_url(url, params)
        self.assertEqual('https://www.foo.com/?access_token=bar&foo=bar', processed_url)

    def test_slashes_are_properly_prepended(self):
        slashTestOne = FacebookUrlManipulator.force_slash_prefix('foo')
        slashTestTwo = FacebookUrlManipulator.force_slash_prefix('/foo')
        slashTestThree = FacebookUrlManipulator.force_slash_prefix('foo/bar')
        slashTestFour = FacebookUrlManipulator.force_slash_prefix('/foo/bar')
        slashTestFive = FacebookUrlManipulator.force_slash_prefix(None)
        slashTestSix = FacebookUrlManipulator.force_slash_prefix('')
        self.assertEqual('/foo', slashTestOne)
        self.assertEqual('/foo', slashTestTwo)
        self.assertEqual('/foo/bar', slashTestThree)
        self.assertEqual('/foo/bar', slashTestFour)
        self.assertEqual(None, slashTestFive)
        self.assertEqual('', slashTestSix)

    def test_params_can_be_returned_as_array(self):
        paramsOne = FacebookUrlManipulator.get_params_as_array('/foo')
        paramsTwo = FacebookUrlManipulator.get_params_as_array('/foo?one=1&two=2')
        paramsThree = FacebookUrlManipulator.get_params_as_array('https://www.foo.com')
        paramsFour = FacebookUrlManipulator.get_params_as_array('https://www.foo.com/?')
        paramsFive = FacebookUrlManipulator.get_params_as_array('https://www.foo.com/?foo=bar')
        self.assertEqual({}, paramsOne)
        self.assertEqual({'one': '1', 'two': '2'}, paramsTwo)
        self.assertEqual({}, paramsThree)
        self.assertEqual({}, paramsFour)
        self.assertEqual({'foo': 'bar'}, paramsFive)

    mergable_endpoints = lambda : (
        (
            'https://www.foo.com/?foo=ignore_foo&dance=fun',
            '/me?foo=keep_foo',
            '/me?dance=fun&foo=keep_foo',
        ),
        (
            'https://www.bar.com?',
            'https://foo.com?foo=bar',
            'https://foo.com?foo=bar',
        ),
        (
            'you',
            'me',
            'me',
        ),
        (
            '/1234?swing=fun',
            '/1337?bar=baz&west=coast',
            '/1337?bar=baz&swing=fun&west=coast',
        ),
    )

    @data_provider(mergable_endpoints)
    def test_params_can_be_merged_onto_url_properly(self, url_one, url_two, expected):
        result = FacebookUrlManipulator.merge_url_params(url_one, url_two)
        self.assertEqual(result, expected)

    def testGraphUrlsCanBeTrimmed(self):
        full_graph_url = 'https://graph.facebook.com/'
        base_graph_url = FacebookUrlManipulator.base_graph_url_endpoint(full_graph_url)
        self.assertEqual('/', base_graph_url)

        full_graph_url = 'https://graph.facebook.com/v1.0/'
        base_graph_url = FacebookUrlManipulator.base_graph_url_endpoint(full_graph_url)
        self.assertEqual('/', base_graph_url)

        full_graph_url = 'https://graph.facebook.com/me'
        base_graph_url = FacebookUrlManipulator.base_graph_url_endpoint(full_graph_url)
        self.assertEqual('/me', base_graph_url)

        full_graph_url = 'https://graph.beta.facebook.com/me'
        base_graph_url = FacebookUrlManipulator.base_graph_url_endpoint(full_graph_url)
        self.assertEqual('/me', base_graph_url)

        full_graph_url = 'https://whatever-they-want.facebook.com/v2.1/me'
        base_graph_url = FacebookUrlManipulator.base_graph_url_endpoint(full_graph_url)
        self.assertEqual('/me', base_graph_url)

        full_graph_url = 'https://graph.facebook.com/v5.301/1233?foo=bar'
        base_graph_url = FacebookUrlManipulator.base_graph_url_endpoint(full_graph_url)
        self.assertEqual('/1233?foo=bar', base_graph_url)
