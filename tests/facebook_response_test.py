# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tests import PythonFacebookTestCase
from python_facebook.sdk.exceptions.facebook_response_exception import \
    FacebookResponseException
from python_facebook.sdk.graph_nodes.graph_node import GraphNode
from python_facebook.sdk.response import FacebookResponse

from python_facebook.sdk.facebook_app import FacebookApp
from python_facebook.sdk.request import FacebookRequest


class FacebookResponseTest(PythonFacebookTestCase):
    def setUp(self):
        super(FacebookResponseTest, self).setUp()
        app = FacebookApp('123', 'foo_secret')
        self.request = FacebookRequest(app, 'foo_token', method='GET',
                                       endpoint='/me/photos?keep=me',
                                       params={'foo': 'bar'}, e_tag='foo_eTag',
                                       graph_version='v1337')

    def testAnETagCanBeProperlyAccessed(self):
        response = FacebookResponse(self.request, '', 200, {'ETag': 'foo_tag'})
        eTag = response.get_e_tag()
        self.assertEqual('foo_tag', eTag)

    def testAProperAppSecretProofCanBeGenerated(self):
        response = FacebookResponse(self.request)
        appSecretProof = response.get_app_secret_proof()
        self.assertEqual(
            'df4256903ba4e23636cc142117aa632133d75c642bd2a68955be1443bd14deb9',
            appSecretProof)

    def testASuccessfulJsonResponseWillBeDecodedToAGraphNode(self):
        graphResponseJson = '{"id":"123","name":"Foo"}'
        response = FacebookResponse(self.request, graphResponseJson, 200)
        decodedResponse = response.get_decoded_body()
        graphNode = response.get_graph_node()
        self.assertFalse(response.is_error(),
                         'Did not expect Response to return an error.')
        self.assertEqual({
            'id': '123',
            'name': 'Foo',
        }, decodedResponse)
        self.assertIsInstance(graphNode, GraphNode)

    def testASuccessfulJsonResponseWillBeDecodedToAGraphEdge(self):
        graphResponseJson = '{"data":[{"id":"123","name":"Foo"},' \
                            '{"id":"1337","name":"Bar"}]}'
        response = FacebookResponse(self.request, graphResponseJson, 200)
        graphEdge = response.get_graph_edge()
        self.assertFalse(response.is_error(),
                         'Did not expect Response to return an error.')
        self.assertIsInstance(graphEdge[0], GraphNode)
        self.assertIsInstance(graphEdge[1], GraphNode)

    def testASuccessfulUrlEncodedKeyValuePairResponseWillBeDecoded(self):
        graphResponseKeyValuePairs = 'id=123&name=Foo'
        response = FacebookResponse(self.request, graphResponseKeyValuePairs,
                                    200)
        decodedResponse = response.get_decoded_body()
        self.assertFalse(response.is_error(),
                         'Did not expect Response to return an error.')
        self.assertEqual({
            'id': '123',
            'name': 'Foo',
        }, decodedResponse)

    def testErrorStatusCanBeCheckedWhenAnErrorResponseIsReturned(self):
        graphResponse = '{"error":{"message":"Foo error.",' \
                        '"type":"OAuthException",' \
                        '"code":190,"error_subcode":463}}'
        response = FacebookResponse(self.request, graphResponse, 401)
        exception = response.get_thrown_exception()
        self.assertTrue(response.is_error(),
                        'Expected Response to return an error.')
        self.assertIsInstance(exception, FacebookResponseException)
