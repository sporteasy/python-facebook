# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib
from collections import OrderedDict
from time import time
from python_facebook.sdk.http.request_body import RequestBody


class RequestBodyMultipart(RequestBody):
    def __init__(self, params=None, files=None, boundary=None):
        self.params = params or {}
        self.files = files or {}
        self.boundary = boundary or self._uniqid()

    def _uniqid(self):
        return hex(int(time()))[2:10] + hex(int(time()*1000000) % 0x100000)[2:7]

    def get_body(self):
        body = ''
        # Compile normal params
        params = self.__get_nested_params(self.params)
        for key, val in params.items():
            body += self.__get_param_string(key, val)

        # Compile files
        for key, val in self.files.items():
            body += self.__get_file_string(key, val)

        # Peace out
        body += "--{}--\r\n".format(self.boundary)

        return body

    def get_boundary(self):
        return self.boundary

    def __get_file_string(self, name, file):
        return "--{}\r\nContent-Disposition: form-data; name=\"{}\"; filename=\"{}\"{}\r\n\r\n{}\r\n".format(
            self.boundary, name, file.get_file_name(), self.__get_file_headers(file), file.get_contents())

    def __get_param_string(self, name, value):
        return "--{}\r\nContent-Disposition: form-data; name=\"{}\"\r\n\r\n{}\r\n".format(self.boundary, name, value)

    def __get_nested_params(self, params):
        def _build_nested_params(_params, _output, _base_key=None):
            # build params with key looking like PHP ones, eg `form[field1][field2][field3]`
            for _key, _value in _params.items():
                if isinstance(_value, (basestring, int, long)):
                    if _base_key:
                        _output_key = '{}[{}]'.format(_base_key, _key)
                    else:
                        _output_key = _key
                    _output[_output_key] = _value
                elif isinstance(_value, list):
                    _i = 0
                    for _element in _value:
                        if _base_key:
                            _output_key = '{}[{}]'.format(_base_key, _key)
                        else:
                            _output_key = _key
                        _output_key = '{}[{}]'.format(_output_key, _i)
                        _output[_output_key] = _element
                        _i += 1
                elif isinstance(_value, dict):
                    if _base_key:
                        _output_key = '{}[{}]'.format(_base_key, _key)
                    else:
                        _output_key = _key
                    _output = _build_nested_params(_value, _output, _output_key)

            return _output

        output = _build_nested_params(params, OrderedDict())
        return output

    def __get_file_headers(self, file):
        return "\r\nContent-Type: {}".format(file.get_mime_type())
