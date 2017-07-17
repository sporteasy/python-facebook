# -*- coding: utf-8 -*-
import urllib
import hmac
import hashlib
import requests
import urlparse

from simplejson import JSONDecodeError

from python_facebook.sdk.response import FacebookResponse, QueryStringDictFormatter
from python_facebook.sdk.session import FacebookSession
from python_facebook.sdk.exceptions.facebook_response_exception import FacebookResponseException


class FacebookRequest(object):
    """
    Do not use directly, use python_facebook.adapters.FacebookRequest instead
    """

    CLIENT_VERSION = '1.0'

    GRAPH_API_VERSION = 'v2.9'

    BASE_GRAPH_URL = 'https://graph.facebook.com'

    BASE_VIDEO_GRAPH_URL = 'https://graph-video.facebook.com'

    def __init__(self, app_id, app_secret, session, method, path, params=None, version=None,
                 etag=None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.session = session
        self.method = method
        self.path = path
        self.version = version or self.GRAPH_API_VERSION
        self.etag = etag
        params = params or {}

        if session and not params.get('access_token'):
            params['access_token'] = session.get_token()

        if not params.get('appsecret_proof') and FacebookSession.use_app_secret_proof():
            params['appsecret_proof'] = self.get_app_secret_proof(params['access_token'])

        self.params = params
        self.request_count = 0

    def execute(self):
        """
        Makes the request to Facebook and returns the result.

        :return FacebookResponse:
        """
        url = self._get_request_url()
        payload = self.get_parameters()

        if self.method == 'GET':
            url = self.append_params_to_url(url, payload)
            payload = {}

        headers = {
            'User-Agent': 'fb-python-' + self.CLIENT_VERSION,
            'Accept-Encoding': '*'
        }
        if self.etag is not None:
            headers.update({'If-None-Match': self.etag})

        method = getattr(requests, self.method.lower())
        response = method(url, data=payload, headers=headers)

        self.request_count += 1

        etag_hit = 304 == response.status_code
        etag_received = response.headers.get('ETag', None)
        raw_text_result = response.text
        try:
            decoded_result = response.json()
        except JSONDecodeError as exc:
            data = urlparse.parse_qs(raw_text_result)
            return FacebookResponse(self, data, raw_text_result, etag_hit, etag_received)

        if 'error' in decoded_result:
            raise FacebookResponseException.create(response)

        return FacebookResponse(self, decoded_result, raw_text_result, etag_hit, etag_received)

    def _get_request_url(self):
        """
        Returns the base Graph URL.

        :return string:
        """
        path_elements = self.path.split('/')
        last_in_path = path_elements[-1]
        if last_in_path == 'videos' and self.method == 'POST':
            base_url = self.BASE_VIDEO_GRAPH_URL
            raise NotImplemented
        else:
            base_url = self.BASE_GRAPH_URL

        return base_url + '/' + self.version + self.path

    def get_parameters(self):
        return self.params

    def get_app_secret_proof(self, token):
        """
        Generate and return the appsecret_proof value for an access_token

        :param token:
        :return:
        """
        app_secret = FacebookSession.get_target_app_secret(self.app_secret)
        h = hmac.new(app_secret, token, hashlib.sha256)
        return h.hexdigest()

    @staticmethod
    def append_params_to_url(url, params):
        """
        Gracefully appends params to the URL.

        :param url:
        :param params:
        :return string:
        """
        if not params:
            return url

        if '?' not in url:
            return url + '?' + urllib.urlencode(sorted(params.items()))

        path, query_string = url.split('?')
        query_params = QueryStringDictFormatter(urlparse.parse_qs(query_string)).output
        # Favor query_params from the original URL over params
        params.update(query_params)

        return path + '?' + urllib.urlencode(sorted(params.items()))
