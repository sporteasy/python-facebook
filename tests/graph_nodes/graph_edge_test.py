# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tests import PythonFacebookTestCase
from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException
from python_facebook.sdk.facebook_app import FacebookApp
from python_facebook.sdk.graph_nodes.graph_edge import GraphEdge
from python_facebook.sdk.graph_nodes.graph_node import GraphNode
from python_facebook.sdk.request import FacebookRequest


class GraphEdgeTest(PythonFacebookTestCase):
    pagination = {
        'next': 'https://graph.facebook.com/v7.12/998899/photos?pretty=0&limit=25&after=foo_after_cursor',
        'previous': 'https://graph.facebook.com/v7.12/998899/photos?pretty=0&limit=25&before=foo_before_cursor',
    }

    def setUp(self):
        super(GraphEdgeTest, self).setUp()
        app = FacebookApp('123', 'foo_app_secret')
        self.request = FacebookRequest(app, 'foo_token', 'GET', '/me/photos?keep=me', {'foo': 'bar'}, 'foo_eTag', 'v1337')

    def testNonGetRequestsWillThrow(self):
        self.request.set_method('POST')
        graphEdge = GraphEdge(self.request)
        with self.assertRaises(FacebookSDKException):
            graphEdge.validate_for_pagination()

    def testCanReturnGraphGeneratedPaginationEndpoints(self):
        graphEdge = GraphEdge(self.request, metadata={'paging': self.pagination})
        nextPage = graphEdge.get_pagination_url('next')
        prevPage = graphEdge.get_pagination_url('previous')
        self.assertEqual('/998899/photos?pretty=0&limit=25&after=foo_after_cursor', nextPage)
        self.assertEqual('/998899/photos?pretty=0&limit=25&before=foo_before_cursor', prevPage)

    def testCanInstantiateNewPaginationRequest(self):
        graphEdge = GraphEdge(self.request, metadata={'paging': self.pagination}, parent_edge_endpoint='/1234567890/likes')
        nextPage = graphEdge.get_next_page_request()
        prevPage = graphEdge.get_previous_page_request()
        self.assertIsInstance(nextPage, FacebookRequest)
        self.assertIsInstance(prevPage, FacebookRequest)
        self.assertNotEqual(self.request, nextPage)
        self.assertNotEqual(self.request, prevPage)
        expected = '/v1337/998899/photos?access_token=foo_token&after=foo_after_cursor&appsecret_proof=857d5f035a894f16b4180f19966e055cdeab92d4d53017b13dccd6d43b6497af&foo=bar&limit=25&pretty=0'
        self.assertEqual(expected, nextPage.get_url())
        expected = '/v1337/998899/photos?access_token=foo_token&appsecret_proof=857d5f035a894f16b4180f19966e055cdeab92d4d53017b13dccd6d43b6497af&before=foo_before_cursor&foo=bar&limit=25&pretty=0'
        self.assertEqual(expected, prevPage.get_url())

    def testCanMapOverNodes(self):
        graphEdge = GraphEdge(self.request,
            [
                GraphNode({'name': 'dummy'}),
                GraphNode({'name': 'dummy'}),
            ],
            {'paging': self.pagination},
            '/1234567890/likes'
        )
        def _lambda(_node):
            _node.set_field('name', _node.get_field('name').replace('dummy', 'foo'))
            return _node
        graphEdge = graphEdge.map(_lambda)

        graphEdgeToCompare = GraphEdge(
            self.request,
            [
                GraphNode({'name': 'foo'}),
                GraphNode({'name': 'foo'})
            ],
            {'paging': self.pagination},
            '/1234567890/likes'
        )
        self.assertEqual(graphEdgeToCompare, graphEdge)
