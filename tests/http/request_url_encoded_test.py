# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from python_facebook.sdk.http.request_body_url_encoded import RequestBodyUrlEncoded


class RequestUrlEncodedTest(unittest.TestCase):

    def testCanProperlyEncodeAnArrayOfParams(self):
        message = RequestBodyUrlEncoded({
            'foo': 'bar',
            'scawy_vawues': '@FooBar is a real twitter handle.',
        })
        body = message.get_body()
        self.assertEqual('foo=bar&scawy_vawues=%40FooBar+is+a+real+twitter+handle.', body)

    def testSupportsMultidimensionalParams(self):
        message = RequestBodyUrlEncoded({
            'faz': [1, 2, 3],
            'foo': 'bar',
            'targeting': {
                'age_min': 13,
                'countries': 'US,GB',
            },
            'call_to_action': {
                'type': 'LEARN_MORE',
                'value': {
                    'link': 'http://example.com',
                    'sponsorship': {
                        'image': 'http://example.com/bar.jpg',
                    },
                },
            },
        })
        body = message.get_body()
        self.assertEqual(
            'faz%5B0%5D=1&faz%5B1%5D=2&faz%5B2%5D=3&foo=bar&targeting%5Bcountries%5D=US%2CGB&targeting%5Bage_min%5D=13&call_to_action%5Btype%5D=LEARN_MORE&call_to_action%5Bvalue%5D%5Blink%5D=http%3A%2F%2Fexample.com&call_to_action%5Bvalue%5D%5Bsponsorship%5D%5Bimage%5D=http%3A%2F%2Fexample.com%2Fbar.jpg', body)
