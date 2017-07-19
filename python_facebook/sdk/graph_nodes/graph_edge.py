import copy

from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException
from python_facebook.sdk.graph_nodes.base_graph_collection import BaseCollection
from python_facebook.sdk.url.facebook_url_manipulator import FacebookUrlManipulator


class GraphEdge(BaseCollection):

    def __init__(self, request, data=None, metadata=None,
                 parent_edge_endpoint=None, subclass_name=None):
        self.request = request

        if metadata is None:
            metadata = {}
        self.metadata = metadata
        self.parent_edge_endpoint = parent_edge_endpoint
        self.subclass_name = subclass_name

        super(GraphEdge, self).__init__(data)

    def get_parent_graph_edge(self):
        return self.parent_edge_endpoint

    def get_subclass_name(self):
        return self.subclass_name

    def get_metadata(self):
        return self.metadata

    def get_next_cursor(self):
        return self.get_cursor('after')

    def get_previous_cursor(self):
        return self.get_cursor('before')

    def get_cursor(self, direction):
        """
        Returns the cursor for a specific direction if it exists.
        """
        try:
            return self.metadata['paging']['cursors'][direction]
        except KeyError:
            return None

    def get_pagination_url(self, direction):
        self.validate_for_pagination()
        if 'paging' in self.metadata and not self.metadata['paging'].get(direction):
            return None
        return FacebookUrlManipulator.base_graph_url_endpoint(self.metadata['paging'].get(direction))

    def validate_for_pagination(self):
        if self.request.get_method() != 'GET':
            raise FacebookSDKException('You can only paginate on a GET request.', 720)

    def get_pagination_request(self, direction):
        page_url = self.get_pagination_url(direction)
        if not page_url:
            return None

        new_request = copy.deepcopy(self.request)
        new_request.set_endpoint(page_url)

        return new_request

    def get_next_page_request(self):
        return self.get_pagination_request('next')

    def get_previous_page_request(self):
        return self.get_pagination_request('previous')

    def get_total_count(self):
        try:
            return self.metadata['summary']['total_count']
        except KeyError:
            return None

    def map(self, callback):
        if isinstance(self.items, dict):
            items = {key: callback(value) for key, value in self.items.items()}
        else:
            items = [callback(value) for value in self.items]
        return GraphEdge(self.request, items, self.metadata, self.parent_edge_endpoint, self.subclass_name)
