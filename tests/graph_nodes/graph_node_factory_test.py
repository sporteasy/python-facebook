# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import json

from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException
from python_facebook.sdk.graph_nodes.graph_edge import GraphEdge
from python_facebook.sdk.graph_nodes.graph_node import GraphNode
from python_facebook.sdk.graph_nodes.graph_node_factory import GraphNodeFactory
from python_facebook.sdk.response import FacebookResponse

from python_facebook.sdk.facebook_app import FacebookApp
from python_facebook.sdk.request import FacebookRequest
from tests.fixtures.my_foo_graph_node import MyFooGraphNode
from tests.fixtures.my_foo_sub_class_graph_node import MyFooSubClassGraphNode


class GraphNodeFactoryTest(unittest.TestCase):
    def setUp(self):
        app = FacebookApp('123', 'foo_app_secret')
        self.request = FacebookRequest(app, 'foo_token', 'GET', '/me/photos?keep=me', {'foo': 'bar'}, 'foo_eTag', 'v1337')

    def testAValidGraphNodeResponseWillNotThrow(self):
        data = '{"id":"123","name":"foo"}'
        res = FacebookResponse(self.request, data)
        factory = GraphNodeFactory(res)
        factory.validate_response_castable_as_graph_node()

    def testANonGraphNodeResponseWillThrow(self):
        data = '{"data":[{"id":"123","name":"foo"},{"id":"1337","name":"bar"}]}'
        res = FacebookResponse(self.request, data)
        factory = GraphNodeFactory(res)
        with self.assertRaises(FacebookSDKException):
            factory.validate_response_castable_as_graph_node()

    def testAValidGraphEdgeResponseWillNotThrow(self):
        data = '{"data":[{"id":"123","name":"foo"},{"id":"1337","name":"bar"}]}'
        res = FacebookResponse(self.request, data)
        factory = GraphNodeFactory(res)
        factory.validate_response_castable_as_graph_edge()

    def testANonGraphEdgeResponseWillThrow(self):
        data = '{"id":"123","name":"foo"}'
        res = FacebookResponse(self.request, data)
        factory = GraphNodeFactory(res)
        with self.assertRaises(FacebookSDKException):
            factory.validate_response_castable_as_graph_edge()

    def testOnlyNumericArraysAreCastableAsAGraphEdge(self):
        shouldPassOne = GraphNodeFactory.is_castable_as_graph_edge({})
        shouldPassTwo = GraphNodeFactory.is_castable_as_graph_edge(['foo', 'bar'])
        shouldFail = GraphNodeFactory.is_castable_as_graph_edge({'faz': 'baz'})
        self.assertTrue(shouldPassOne, 'Expected the given array to be castable as a GraphEdge.')
        self.assertTrue(shouldPassTwo, 'Expected the given array to be castable as a GraphEdge.')
        self.assertFalse(shouldFail, 'Expected the given array to not be castable as a GraphEdge.')

    def testCastingAsASubClassObjectWillInstantiateTheSubClass(self):
        data = '{"id":"123","name":"foo"}'
        res = FacebookResponse(self.request, data)
        factory = GraphNodeFactory(res)
        mySubClassObject = factory.make_graph_node('tests.fixtures.my_foo_graph_node.MyFooGraphNode')
        self.assertIsInstance(mySubClassObject, MyFooGraphNode)

    def testASubClassMappingWillAutomaticallyInstantiateSubClass(self):
        data = '{"id":"123","name":"Foo Name","foo_object":{"id":"1337","name":"Should be sub classed!"}}'
        res = FacebookResponse(self.request, data)
        factory = GraphNodeFactory(res)
        mySubClassObject = factory.make_graph_node('tests.fixtures.my_foo_graph_node.MyFooGraphNode')
        fooObject = mySubClassObject.get_field('foo_object')
        self.assertIsInstance(mySubClassObject, MyFooGraphNode)
        self.assertIsInstance(fooObject, MyFooSubClassGraphNode)

    def testAnUnknownGraphNodeWillBeCastAsAGenericGraphNode(self):
        data = json.dumps({
            'id': '123',
            'name': 'Foo Name',
            'unknown_object': {
                'id': '1337',
                'name': 'Should be generic!',
            }
        })
        res = FacebookResponse(self.request, data)
        factory = GraphNodeFactory(res)
        mySubClassObject = factory.make_graph_node('tests.fixtures.my_foo_graph_node.MyFooGraphNode')
        unknownObject = mySubClassObject.get_field('unknown_object')
        self.assertIsInstance(mySubClassObject, MyFooGraphNode)
        self.assertIsInstance(unknownObject, GraphNode)
        self.assertNotIsInstance(unknownObject, MyFooGraphNode)

    def testAListFromGraphWillBeCastAsAGraphEdge(self):
        data = json.dumps({
            'data': [
                {
                    'id': '123',
                    'name': 'Foo McBar',
                    'link': 'http://facebook/foo',
                },
                {
                    'id': '1337',
                    'name': 'Bar McBaz',
                    'link': 'http://facebook/bar',
                },
            ],
            'paging': {
                'next': 'http://facebook/next',
                'previous': 'http://facebook/prev',
            },
        })
        res = FacebookResponse(self.request, data)
        factory = GraphNodeFactory(res)
        graphEdge = factory.make_graph_edge()
        graphData = graphEdge.as_array()
        self.assertIsInstance(graphEdge, GraphEdge)

        self.assertEquals(json.dumps({
            'id': '123',
            'name': 'Foo McBar',
            'link': 'http://facebook/foo',
        }), graphData[0].as_json())
        self.assertEquals(json.dumps({
            'id': '1337',
            'name': 'Bar McBaz',
            'link': 'http://facebook/bar',
        }), graphData[1].as_json())

    def testAGraphNodeWillBeCastAsAGraphNode(self):
        data = json.dumps({
            'id': '123',
            'name': 'Foo McBar',
            'link': 'http://facebook/foo',
        })
        res = FacebookResponse(self.request, data)
        factory = GraphNodeFactory(res)
        graphNode = factory.make_graph_node()
        graphData = graphNode.as_array()
        self.assertIsInstance(graphNode, GraphNode)
        self.assertEquals({
            'id': '123',
            'name': 'Foo McBar',
            'link': 'http://facebook/foo',
        }, graphData)

    def testAGraphNodeWithARootDataKeyWillBeCastAsAGraphNode(self):
        data = json.dumps({
            'data': {
                'id': '123',
                'name': 'Foo McBar',
                'link': 'http://facebook/foo',
            },
        })
        res = FacebookResponse(self.request, data)
        factory = GraphNodeFactory(res)
        graphNode = factory.make_graph_node()
        graphData = graphNode.as_array()
        self.assertIsInstance(graphNode, GraphNode)
        self.assertEquals({
            'id': '123',
            'name': 'Foo McBar',
            'link': 'http://facebook/foo',
        }, graphData)

    def testAGraphEdgeWillBeCastRecursively(self):
        someUser = {
            'id': '123',
            'name': 'Foo McBar',
        }
        likesCollection = {
            'data': [
                {
                    'id': '1',
                    'name': 'Sammy Kaye Powers',
                    'is_sexy': True,
                },
                {
                    'id': '2',
                    'name': 'Yassine Guedidi',
                    'is_sexy': True,
                },
                {
                    'id': '3',
                    'name': 'Fosco Marotto',
                    'is_sexy': True,
                },
                {
                    'id': '4',
                    'name': 'Foo McUgly',
                    'is_sexy': False,
                },
            ],
            'paging': {
                'next': 'http://facebook/next_likes',
                'previous': 'http://facebook/prev_likes',
            },
        }
        commentsCollection = {
            'data': [
                {
                    'id': '42_1',
                    'from': someUser,
                    'message': 'Foo comment.',
                    'created_time': '2014-07-15T03:54:34+0000',
                    'likes': likesCollection,
                },
                {
                    'id': '42_2',
                    'from': someUser,
                    'message': 'Bar comment.',
                    'created_time': '2014-07-15T04:11:24+0000',
                    'likes': likesCollection,
                },
            ],
            'paging': {
                'next': 'http://facebook/next_comments',
                'previous': 'http://facebook/prev_comments',
            },
        }
        dataFromGraph = {
            'data': [
                {
                    'id': '1337_1',
                    'from': someUser,
                    'story': 'Some great foo story.',
                    'likes': likesCollection,
                    'comments': commentsCollection,
                },
                {
                    'id': '1337_2',
                    'from': someUser,
                    'to': {
                        'data': [someUser],
                    },
                    'message': 'Some great bar message.',
                    'likes': likesCollection,
                    'comments': commentsCollection,
                },
            ],
            'paging': {
                'next': 'http://facebook/next',
                'previous': 'http://facebook/prev',
            },
        }
        data = json.dumps(dataFromGraph)
        res = FacebookResponse(self.request, data)
        factory = GraphNodeFactory(res)
        graphNode = factory.make_graph_edge()
        self.assertIsInstance(graphNode, GraphEdge)
        # Story
        storyObject = graphNode[0]
        self.assertIsInstance(storyObject['from'], GraphNode)
        self.assertIsInstance(storyObject['likes'], GraphEdge)
        self.assertIsInstance(storyObject['comments'], GraphEdge)

        # Story Comments
        storyComments = storyObject['comments']
        firstStoryComment = storyComments[0]
        self.assertIsInstance(firstStoryComment['from'], GraphNode)

        # Message
        messageObject = graphNode[1]
        self.assertIsInstance(messageObject['to'], GraphEdge)
        toUsers = messageObject['to']
        self.assertIsInstance(toUsers[0], GraphNode)

    def testAGraphEdgeWillGenerateTheProperParentGraphEdges(self):
        likesList = {
            'data': [
                {
                    'id': '1',
                    'name': 'Sammy Kaye Powers',
                },
            ],
            'paging': {
                'cursors': {
                    'after': 'like_after_cursor',
                    'before': 'like_before_cursor',
                },
            },
        }
        photosList = {
            'data': [
                {
                    'id': '777',
                    'name': 'Foo Photo',
                    'likes': likesList,
                },
            ],
            'paging': {
                'cursors': {
                    'after': 'photo_after_cursor',
                    'before': 'photo_before_cursor',
                },
            },
        }
        data = json.dumps({
            'data': [
                {
                    'id': '111',
                    'name': 'Foo McBar',
                    'likes': likesList,
                    'photos': photosList,
                },
                {
                    'id': '222',
                    'name': 'Bar McBaz',
                    'likes': likesList,
                    'photos': photosList,
                },
            ],
            'paging': {
                'next': 'http://facebook/next',
                'previous': 'http://facebook/prev',
            },
        })
        res = FacebookResponse(self.request, data)
        factory = GraphNodeFactory(res)
        graphEdge = factory.make_graph_edge()
        topGraphEdge = graphEdge.get_parent_graph_edge()
        childGraphEdgeOne = graphEdge[0]['likes'].get_parent_graph_edge()
        childGraphEdgeTwo = graphEdge[1]['likes'].get_parent_graph_edge()
        childGraphEdgeThree = graphEdge[1]['photos'].get_parent_graph_edge()
        childGraphEdgeFour = graphEdge[1]['photos'][0]['likes'].get_parent_graph_edge()
        self.assertIsNone(topGraphEdge)
        self.assertEquals('/111/likes', childGraphEdgeOne)
        self.assertEquals('/222/likes', childGraphEdgeTwo)
        self.assertEquals('/222/photos', childGraphEdgeThree)
        self.assertEquals('/777/likes', childGraphEdgeFour)
