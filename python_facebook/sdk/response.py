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
    def __init__(self, request, body=None, http_status_code=None, headers=None):
        self.request = request
        self.body = body
        self.http_status_code = http_status_code
        self.headers = headers or {}

        self.decode_body()

    def get_request(self):
        return self.request

    def get_app(self):
        return self.request.get_app()

    def get_access_token(self):
        return self.request.get_access_token()

    def get_http_status_code(self):
        return self.http_status_code

    def get_headers(self):
        return self.headers

    def get_body(self):
        return self.body

    def get_decoded_body(self):
        return self.decoded_body

    def get_app_secret_proof(self):
        return self.request.get_app_secret_proof()

    def get_e_tag(self):
        return self.headers.get('ETag', None)

    def get_graph_version(self):
        return self.headers.get('Facebook-API-Version', None)

    def is_error(self):
        return 'error' in self.decoded_body

    def throw_exception(self):
        raise self.thrown_exception

    def make_exception(self):
        self.thrown_exception = FacebookResponseException.create(self)

    def get_thrown_exception(self):
        return self.thrown_exception

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
                self.decoded_body = {key: val[0] for key, val in self.decoded_body.items()}
            except ValueError:
                if is_bool(self.body):
                    self.decoded_body = {'success': to_boolean(self.body)}
                elif is_number(self.body):
                    self.decoded_body = {'id': self.body}

        if self.is_error():
            self.make_exception()

    def get_graph_object(self, subclass_name=None):
        return self.get_graph_node(subclass_name)

    def get_graph_node(self, subclass_name=None):
        factory = GraphNodeFactory(self)
        return factory.make_graph_node(subclass_name)

    def get_graph_album(self):
        factory = GraphNodeFactory(self)
        return factory.make_graph_album()

    def get_graph_page(self):
        factory = GraphNodeFactory(self)
        return factory.make_graph_page()

    def get_graph_session_info(self):
        factory = GraphNodeFactory(self)
        return factory.make_graph_session_info()

    def get_graph_user(self):
        factory = GraphNodeFactory(self)
        return factory.make_graph_user()

    def get_graph_event(self):
        factory = GraphNodeFactory(self)
        return factory.make_graph_event()

    def get_graph_group(self):
        factory = GraphNodeFactory(self)
        return factory.make_graph_group()

    def get_graph_list(self, subclass_name=None, auto_prefix=True):
        return self.get_graph_edge(subclass_name, auto_prefix)

    def get_graph_edge(self, subclass_name=None, auto_prefix=True):
        factory = GraphNodeFactory(self)
        return factory.make_graph_edge(subclass_name, auto_prefix)


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_bool(s):
    return s in (True, 'true', 'True', 1, '1', 'on', 'On',
                 False, 'false', 'False', 0, '0', 'off', 'Off')


def to_boolean(s):
    return s in (True, 'true', 'True', 1, '1', 'on', 'On')
