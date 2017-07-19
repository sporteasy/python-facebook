# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from requests.structures import CaseInsensitiveDict


class GraphRawResponse(object):

    def __init__(self, headers, body, http_status_code=None):
        self.headers = {}
        self.http_response_code = None
        if isinstance(http_status_code, (int, long)):
            self.http_response_code = int(http_status_code)

        if isinstance(headers, (dict, CaseInsensitiveDict)):
            self.headers = headers
        else:
            self.__set_headers_from_string(headers)
        self.body = body

    def get_headers(self):
        return self.headers

    def get_body(self):
        return self.body

    def get_http_response_code(self):
        return self.http_response_code

    def set_http_response_code_from_header(self, raw_response_header):
        # ex: HTTP/1.1 200 OK
        pattern = '^HTTP/\d\.\d\s+(\d+)\s+.*'

        result = re.match(pattern, raw_response_header)
        self.http_response_code = int(result.group(1))

    def __set_headers_from_string(self, raw_headers):
        # Normalize line breaks
        raw_headers = raw_headers.replace("\r\n", "\n")
        # There will be multiple headers if a 301 was followed
        # or a proxy was followed, etc
        header_collection = raw_headers.strip().split("\n\n")
        # We just want the last response(at the end)
        raw_header = header_collection[-1]
        header_components = raw_header.split("\n")
        for line in header_components:
            if ':' not in line:
                self.set_http_response_code_from_header(line)
            else:
                idx = line.index(': ')
                key = line[:idx].strip()
                value = line[idx + 2:].strip()
                self.headers.update({
                    key: value
                })
