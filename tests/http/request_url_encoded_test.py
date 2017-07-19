# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from tests import PythonFacebookTestCase
from python_facebook.sdk.http.request_body_url_encoded import \
    RequestBodyUrlEncoded


class RequestUrlEncodedTest(PythonFacebookTestCase):

    def testCanProperlyEncodeAnArrayOfParams(self):
        message = RequestBodyUrlEncoded(OrderedDict({
            'foo': 'bar',
            'scawy_vawues': '@FooBar is a real twitter handle.',
        }))
        body = message.get_body()

        exp = 'foo=bar&scawy_vawues=%40FooBar+is+a+real+twitter+handle.'
        expected = sorted(exp.split('&'))
        self.assertEqual(expected, sorted(body.split('&')))

    def testSupportsMultidimensionalParams(self):
        message = RequestBodyUrlEncoded(OrderedDict({
            'faz': [1, 2, 3],
            'foo': 'bar',
            'targeting': OrderedDict({
                'age_min': 13,
                'countries': 'US,GB',
            }),
            'call_to_action': OrderedDict({
                'type': 'LEARN_MORE',
                'value': OrderedDict({
                    'link': 'http://example.com',
                    'sponsorship': {
                        'image': 'http://example.com/bar.jpg',
                    },
                }),
            }),
        }))
        body = message.get_body()

        exp = 'faz%5B0%5D=1&faz%5B1%5D=2&faz%5B2%5D=3&foo=bar&targeting%5B' \
              'countries%5D=US%2CGB&targeting%5Bage_min%5D=13&call_to_acti' \
              'on%5Btype%5D=LEARN_MORE&call_to_action%5Bvalue%5D%5Blink%5D' \
              '=http%3A%2F%2Fexample.com&call_to_action%5Bvalue%5D%5Bspons' \
              'orship%5D%5Bimage%5D=http%3A%2F%2Fexample.com%2Fbar.jpg'
        expected = sorted(exp.split('&'))
        self.assertEqual(expected, sorted(body.split('&')))
