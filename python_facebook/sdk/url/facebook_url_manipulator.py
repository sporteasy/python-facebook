# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import urlparse
import urllib
from python_facebook.sdk.response import QueryStringDictFormatter


class FacebookUrlManipulator(object):

    @staticmethod
    def remove_params_from_url(url, params_to_filter):
        if not url:
            return url
        parsed = urlparse.urlparse(url)
        params = {}
        if parsed.query:
            for key, value in urlparse.parse_qs(parsed.query).items():
                if key not in params_to_filter:
                    params[key] = value[0]
        port = '' if not parsed.port else ':{}'.format(parsed.port)
        url = '{scheme}://{host}{port}{path}'.format(scheme=parsed.scheme, host=parsed.hostname,
                                                     port=port, path=parsed.path)
        return FacebookUrlManipulator.append_params_to_url(url, params)

    @staticmethod
    def append_params_to_url(url, new_params=None):
        if not new_params:
            return url

        if '?' not in url:
            return url + '?' + urllib.urlencode(sorted(new_params.items()))

        path, query_string = url.split('?')
        query_params = QueryStringDictFormatter(urlparse.parse_qs(query_string)).output
        # Favor query_params from the original URL over params
        new_params.update(query_params)

        return path + '?' + urllib.urlencode(sorted(new_params.items()))

    @staticmethod
    def get_params_as_array(url):
        if not url:
            return {}
        parsed = urlparse.urlparse(url)
        parsed_dict = urlparse.parse_qs(parsed.query)
        return {key: value[0] for key, value in parsed_dict.items()}

    @staticmethod
    def merge_url_params(url_to_steal_from, url_to_add_to):
        new_params = FacebookUrlManipulator.get_params_as_array(url_to_steal_from)
        # Nothing new to add, return as- is
        if not new_params:
            return url_to_add_to
        return FacebookUrlManipulator.append_params_to_url(url_to_add_to, new_params)

    @staticmethod
    def force_slash_prefix(string):
        if not string or string[0] == '/':
            return string
        return '/{}'.format(string)

    @staticmethod
    def base_graph_url_endpoint(url_to_trim):
        pattern = '^https?://.+\.facebook\.com(\/v.+?)?/'
        return '/{}'.format(re.sub(pattern, '', url_to_trim))
