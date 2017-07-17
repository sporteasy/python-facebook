from python_facebook.sdk.exceptions import FacebookSDKException


class GraphNodeFactory(object):

    def __init__(self, response):
        self.response = response
        self.decoded_body = response.get_decoded_body()

    def make_graph_node(self, subclass_name):
        self.validate_response_as_array()
        self.validate_response_castable_as_graph_node()
        return self.cast_as_graph_node_or_graph_edge(self.decoded_body, subclass_name)

    def validate_response_as_array(self):
        if not isinstance(self.response, list):
            raise FacebookSDKException('Unable to get response from Graph as array.', 620)

    def validate_response_castable_as_graph_node(self):
        if 'data' in self.decoded_body and self.is_castable_as_graph_edge(self.decoded_body['data']):
            raise FacebookSDKException(
                'Unable to convert response from Graph to a GraphNode because the response looks like a GraphEdge. '
                'Try using GraphNodeFactory.make_graph_edge() instead.',
                620
            )

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
        return data.keys() == range(0, len(data) - 1)
