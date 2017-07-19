# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from tests import PythonFacebookTestCase
from python_facebook.sdk.http.request_body_multipart import RequestBodyMultipart


class RequestBodyMultipartTest(PythonFacebookTestCase):
    maxDiff = None

    def testCanProperlyEncodeAnArrayOfParams(self):
        message = RequestBodyMultipart(params={
            'foo': 'bar',
            'scawy_vawues': '@FooBar is a real twitter handle.',
        }, boundary='foo_boundary')
        body = message.get_body()
        expected_body = "--foo_boundary\r\n"
        expected_body += "Content-Disposition: form-data; name=\"foo\"\r\n\r\nbar\r\n"
        expected_body += "--foo_boundary\r\n"
        expected_body += "Content-Disposition: form-data; name=\"scawy_vawues\"\r\n\r\n@FooBar is a real twitter handle.\r\n"
        expected_body += "--foo_boundary--\r\n"
        self.assertEquals(expected_body, body)
    
    def testCanProperlyEncodeFilesAndParams(self):
        # file = FacebookFile('__DIR__' + '/../foo.txt')
        # message = RequestBodyMultipart(params={
        #     'foo': 'bar',
        # }, files={
        #     'foo_file': file,
        # }, boundary='foo_boundary')
        # body = message.get_body()
        # expected_body = "--foo_boundary\r\n"
        # expected_body += "Content-Disposition: form-data name=\"foo\"\r\n\r\nbar\r\n"
        # expected_body += "--foo_boundary\r\n"
        # expected_body += "Content-Disposition: form-data name=\"foo_file\" filename=\"foo.txt\"\r\n"
        # expected_body += "Content-Type: text/plain\r\n\r\nThis is a text file used for testing. Let's dance.\r\n"
        # expected_body += "--foo_boundary--\r\n"
        # self.assertEquals(expected_body, body)

        #
        # Not implemented yet
        #
        pass
    
    def testSupportsMultidimensionalParams(self):
        message = RequestBodyMultipart(params=OrderedDict({
            'foo': 'bar',
            'faz': [1,2,3],
            'targeting': OrderedDict({
                'countries': 'US,GB',
                'age_min': 13,
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
        }), boundary='foo_boundary')
        body = message.get_body()
        expected_body = "--foo_boundary\r\n"
        expected_body += "Content-Disposition: form-data; name=\"faz[0]\"\r\n\r\n1\r\n"
        expected_body += "--foo_boundary\r\n"
        expected_body += "Content-Disposition: form-data; name=\"faz[1]\"\r\n\r\n2\r\n"
        expected_body += "--foo_boundary\r\n"
        expected_body += "Content-Disposition: form-data; name=\"faz[2]\"\r\n\r\n3\r\n"
        expected_body += "--foo_boundary\r\n"
        expected_body += "Content-Disposition: form-data; name=\"foo\"\r\n\r\nbar\r\n"
        expected_body += "--foo_boundary\r\n"
        expected_body += "Content-Disposition: form-data; name=\"targeting[age_min]\"\r\n\r\n13\r\n"
        expected_body += "--foo_boundary\r\n"
        expected_body += "Content-Disposition: form-data; name=\"targeting[countries]\"\r\n\r\nUS,GB\r\n"
        expected_body += "--foo_boundary\r\n"
        expected_body += "Content-Disposition: form-data; name=\"call_to_action[type]\"\r\n\r\nLEARN_MORE\r\n"
        expected_body += "--foo_boundary\r\n"
        expected_body += "Content-Disposition: form-data; name=\"call_to_action[value][link]\"\r\n\r\nhttp://example.com\r\n"
        expected_body += "--foo_boundary\r\n"
        expected_body += "Content-Disposition: form-data; name=\"call_to_action[value][sponsorship][image]\"\r\n\r\nhttp://example.com/bar.jpg\r\n"
        expected_body += "--foo_boundary--\r\n"
        self.assertEquals(expected_body, body)
