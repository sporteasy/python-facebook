# -*- coding: utf-8 -*-
import json
import sys

from python_facebook.sdk.exceptions.facebook_response_exception import FacebookResponseException
from python_facebook.sdk.graph_nodes.graph_node_factory import GraphNodeFactory


if sys.version_info >= (3, 0):
    import urllib.parse as urlparse
else:
    import urlparse


class QueryStringDictFormatter(object):

    def __init__(self, response_dict):
        self.response_dict = {}
        for key, val in response_dict.items():
            if isinstance(val, list) and len(val) == 1:
                self.response_dict[key] = val[0]
            else:
                self.response_dict[key] = val

    @property
    def output(self):
        return self.response_dict


class FacebookResponse(object):

    def __init__(self, request, body, raw_response, http_status_code=None, headers=None):
        self.request = request
        # self.response_data = QueryStringDictFormatter(body).output
        self.body = body
        self.raw_response = raw_response
        self.http_status_code = http_status_code
        self.headers = headers

        self.decode_body()

    # def get_graph_object(self, cls=None):
    #     if cls is None:
    #         cls = GraphObject
    #     return cls(**self.response_data)

    def get_graph_node(self, subclass_name=None):
        """
        Instantiate a new GraphNode from response.
        """
        factory = GraphNodeFactory(self)
        return factory.make_graph_node(subclass_name)

    def get_decoded_body(self):
        return self.decoded_body

    def decode_body(self):
        """
            Convert the raw response into an array if possible.

            Graph will return 2 types of responses:
                - JSON(P)
                  Most responses from Graph are JSON(P)
                - application/x-www-form-urlencoded key/value pairs
                  Happens on the `/oauth/access_token` endpoint when exchanging
                  a short-lived access token for a long-lived access token
                - And sometimes nothing :/ but that'd be a bug.
        """
        try:
            self.decoded_body = json.loads(self.body)
        except ValueError:
            self.decoded_body = {}

            try:
                self.decoded_body = urlparse.parse_qs(self.body)
            except ValueError:
                if is_number(self.body):
                    self.decoded_body = {'id': self.body}

        if self.is_error():
            self.make_exception()

    def is_error(self):
        return self.decoded_body and 'error' in self.decoded_body

    def make_exception(self):
        self.thrown_exception = FacebookResponseException.create(self)


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
