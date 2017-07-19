# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tests import PythonFacebookTestCase
from python_facebook.sdk.http.graph_raw_response import GraphRawResponse


class GraphRawResponseTest(PythonFacebookTestCase):

    fakeRawProxyHeader = """HTTP/1.0 200 Connection established
    Proxy-agent: Kerio Control/7.1.1 build 1971\r\n\r\n"""

    fakeRawHeader = """HTTP/1.1 200 OK
    Etag: "9d86b21aa74d74e574bbb35ba13524a52deb96e3"
    Content-Type: text/javascript; charset=UTF-8
    X-FB-Rev: 9244768
    Date: Mon, 19 May 2014 18:37:17 GMT
    X-FB-Debug: 02QQiffE7JG2rV6i/Agzd0gI2/OOQ2lk5UW0=
    Access-Control-Allow-Origin: *\r\n\r\n"""

    fakeHeadersAsArray = {
        'Etag': '"9d86b21aa74d74e574bbb35ba13524a52deb96e3"',
        'Content-Type': 'text/javascript; charset=UTF-8',
        'X-FB-Rev': '9244768',
        'Date': 'Mon, 19 May 2014 18:37:17 GMT',
        'X-FB-Debug': '02QQiffE7JG2rV6i/Agzd0gI2/OOQ2lk5UW0=',
        'Access-Control-Allow-Origin': '*',
    }

    jsonFakeHeader = 'x-fb-ads-insights-throttle: {"app_id_util_pct": 0.00,"acc_id_util_pct": 0.00}'
    jsonFakeHeaderAsArray = {'x-fb-ads-insights-throttle': '{"app_id_util_pct": 0.00,"acc_id_util_pct": 0.00}'}

    def testCanSetTheHeadersFromAnArray(self):
        myHeaders = {
            'foo': 'bar',
            'baz': 'faz',
        }
        response = GraphRawResponse(myHeaders, '')
        headers = response.get_headers()
        self.assertEqual(myHeaders, headers)

    def testCanSetTheHeadersFromAString(self):
        response = GraphRawResponse(self.fakeRawHeader, '')
        headers = response.get_headers()
        httpResponseCode = response.get_http_response_code()
        self.assertEqual(self.fakeHeadersAsArray, headers)
        self.assertEqual(200, httpResponseCode)

    def testWillIgnoreProxyHeaders(self):
        response = GraphRawResponse(self.fakeRawProxyHeader + self.fakeRawHeader, '')
        headers = response.get_headers()
        httpResponseCode = response.get_http_response_code()
        self.assertEqual(self.fakeHeadersAsArray, headers)
        self.assertEqual(200, httpResponseCode)

    def testCanTransformJsonHeaderValues(self):
        response = GraphRawResponse(self.jsonFakeHeader, '')
        headers = response.get_headers()
        self.assertEqual(self.jsonFakeHeaderAsArray['x-fb-ads-insights-throttle'], headers[
            'x-fb-ads-insights-throttle'])
