# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException
from python_facebook.sdk.graph_nodes.graph_node import GraphNode
from python_facebook.sdk.utils import get_class


class GraphNodeFactory(object):
    """
     ## Assumptions ##
     GraphEdge - is ALWAYS a numeric array
     GraphEdge - is ALWAYS an array of GraphNode types
     GraphNode - is ALWAYS an associative array
     GraphNode - MAY contain GraphNode's "recurrable"
     GraphNode - MAY contain GraphEdge's "recurrable"
     GraphNode - MAY contain DateTime's "primitives"
     GraphNode - MAY contain string's "primitives"
    """
    BASE_GRAPH_NODE_CLASS = 'python_facebook.sdk.graph_nodes.graph_node.GraphNode'
    BASE_GRAPH_EDGE_CLASS = 'python_facebook.sdk.graph_nodes.graph_edge.GraphEdge'
    BASE_GRAPH_OBJECT_PREFIX = 'graph_nodes'

    def __init__(self, response):
        self.response = response
        self.decoded_body = response.get_decoded_body()

    def make_graph_node(self, subclass_name=None):
        self.validate_response_as_dict()
        self.validate_response_castable_as_graph_node()

        return self.cast_as_graph_node_or_graph_edge(self.decoded_body, subclass_name)

    def make_graph_achievement(self):
        return self.make_graph_node(self.BASE_GRAPH_OBJECT_PREFIX + '.' + 'GraphAchievement')

    def make_graph_album(self):
        return self.make_graph_node(self.BASE_GRAPH_OBJECT_PREFIX + '.' + 'GraphAlbum')

    def make_graph_page(self):
        return self.make_graph_node(self.BASE_GRAPH_OBJECT_PREFIX + '.' + 'GraphPage')

    def make_graph_session_info(self):
        return self.make_graph_node(self.BASE_GRAPH_OBJECT_PREFIX + '.' + 'GraphSessionInfo')

    def make_graph_user(self):
        return self.make_graph_node(self.BASE_GRAPH_OBJECT_PREFIX + '.' + 'GraphUser')

    def make_graph_event(self):
        return self.make_graph_node(self.BASE_GRAPH_OBJECT_PREFIX + '.' + 'GraphEvent')

    def make_graph_group(self):
        return self.make_graph_node(self.BASE_GRAPH_OBJECT_PREFIX + '.' + 'GraphGroup')

    def make_graph_edge(self, subclass_name=None, auto_prefix=True):
        self.validate_response_as_dict()
        self.validate_response_castable_as_graph_node()

        if subclass_name and auto_prefix:
            subclass_name = self.BASE_GRAPH_OBJECT_PREFIX + '.' + subclass_name

        return self.cast_as_graph_node_or_graph_edge(self.decoded_body, subclass_name)

    def validate_response_as_dict(self):
        if not isinstance(self.decoded_body, dict):
            raise FacebookSDKException('Unable to get response from Graph as dict.', 620)

    def validate_response_castable_as_graph_node(self):
        if 'data' in self.decoded_body and self.is_castable_as_graph_edge(self.decoded_body['data']):
            raise FacebookSDKException(
                'Unable to convert response from Graph to a GraphNode because the response looks like a GraphEdge. '
                'Try using GraphNodeFactory.make_graph_edge() instead.',
                620
            )

    def validate_response_castable_as_graph_edge(self):
        if not ('data' in self.decoded_body and self.is_castable_as_graph_edge(self.decoded_body['data'])):
            raise FacebookSDKException(
                'Unable to convert response from Graph to a GraphEdge because the response does not '
                'look like a GraphEdge. '
                'Try using GraphNodeFactory.make_graph_node() instead.',
                620
            )

    def safely_make_graph_node(self, data, subclass_name=None):
        if subclass_name is None:
            subclass_name = self.BASE_GRAPH_NODE_CLASS

        subclass = get_class(subclass_name)
        self.validate_subclass(subclass)

        # Remember the parent node ID
        parent_node_id = data.get('id')

        items = {}

        for key, val in data.items():
            # Array means could be recurable
            if isinstance(val, dict):
                # Detect any smart-casting from the graphObjectMap array.
                # This is always empty on the GraphNode collection, but subclasses can define
                # their own array of smart-casting types.
                graph_object_map = subclass.get_object_map()
                object_subClass = graph_object_map.get(key)

                # Could be a GraphEdge or GraphNode
                items[key] = self.cast_as_graph_node_or_graph_edge(val, object_subClass, key, parent_node_id)
            else:
                items[key] = val

        return subclass(items)

    def cast_as_graph_node_or_graph_edge(self, data, subclass_name=None, parent_key=None, parent_node_id=None):
        """
        Takes an array of values and determines how to cast each node.

        :param data:            The array of data to iterate over.
        :param subclass_name:   The subclass to cast this collection to.
        :param parent_key:      The key of this data (Graph edge).
        :param parent_node_id:  The parent Graph node ID.

        :return: GraphNode|GraphEdge

        :raises FacebookSDKException
        """
        if 'data' in self.decoded_body:
            # Create GraphEdge
            if self.is_castable_as_graph_edge(data['data']):
                return self.safely_make_graph_edge(data, subclass_name, parent_key, parent_node_id)

            # Sometimes Graph is a weirdo and returns a GraphNode under the "data" key
            data = data['data']

        return self.safely_make_graph_node(data, subclass_name)

    def safely_make_graph_edge(self, data, subclass_name=None, parent_key=None, parent_node_id=None):

        if not data.get('data'):
            raise FacebookSDKException('Cannot cast data to GraphEdge. Expected a "data" key.', 620)

        data_list = []

        for graph_node in data['data']:
            data_list.append(self.safely_make_graph_node(graph_node, subclass_name))

        metadata = self.get_metadata(data)

        # We'll need to make an edge endpoint for this in case it's a GraphEdge (for cursor pagination)
        parent_graph_edge_endpoint = '/' + parent_node_id + '/' + parent_key if parent_node_id and parent_key else None
        classname = self.BASE_GRAPH_EDGE_CLASS
        klass = get_class(classname)

        return klass(self.response.get_request(), data_list, metadata, parent_graph_edge_endpoint, subclass_name)

    def get_metadata(self, data):
        data.pop('data')
        return data

    @staticmethod
    def is_castable_as_graph_edge(data):
        """
        Determines whether or not the data should be cast as a GraphEdge.

        :param list data
        :return boolean
        """
        if not data:
            return True

        # Checks for a sequential numeric array which would be a GraphEdge
        # return data.keys() == range(0, len(data) - 1)
        return isinstance(data, list)

    def validate_subclass(self, subclass):
        if issubclass(subclass, GraphNode):
            return

        raise FacebookSDKException(
            'The given subclass "' + subclass + '" is not valid. Cannot cast to an '
            'object that is not a GraphNode subclass.',
            620
        )
