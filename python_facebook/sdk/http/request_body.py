# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class RequestBody(object):
    def get_body(self):
        raise NotImplementedError

    def _build_nested_params(self, params, output, base_key=None):
        # build params with key looking like PHP ones,
        # eg `form[field1][field2][field3]`
        def _check_type(_value):
            try:
                return isinstance(_value, (basestring, int, long))
            except NameError:
                # python3 does not supports basestring
                return isinstance(_value, (str, int, long))

        for key, value in params.items():
            if _check_type(value):
                if base_key:
                    output_key = '{}[{}]'.format(base_key, key)
                else:
                    output_key = key
                output[output_key] = value
            elif isinstance(value, list):
                i = 0
                for element in value:
                    if base_key:
                        output_key = '{}[{}]'.format(base_key, key)
                    else:
                        output_key = key
                    output_key = '{}[{}]'.format(output_key, i)
                    output[output_key] = element
                    i += 1
            elif isinstance(value, dict):
                if base_key:
                    output_key = '{}[{}]'.format(base_key, key)
                else:
                    output_key = key
                output = self._build_nested_params(value, output, output_key)

        return output
