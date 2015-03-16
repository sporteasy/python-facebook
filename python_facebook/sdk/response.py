# -*- coding: utf-8 -*-
from python_facebook.sdk.graph_object import GraphObject


class Formatter(object):

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

    def __init__(self, request, response_data, raw_response, etag_hit=False, etag=None):
        self.request = request
        self.response_data = Formatter(response_data).output
        self.raw_response = raw_response
        self.etag_hit = etag_hit
        self.etag = etag

    def get_graph_object(self, cls=None):
        if cls is None:
            cls = GraphObject
        return cls(**self.response_data)
