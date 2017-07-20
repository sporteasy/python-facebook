# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from collections import OrderedDict

from python_facebook.sdk.http.request_body import RequestBody


class RequestBodyUrlEncoded(RequestBody):
    def __init__(self, params=None):
        self.params = OrderedDict(params or {})

    def get_body(self):
        output = self._build_nested_params(self.params, OrderedDict())
        return urlencode(output)
