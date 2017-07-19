# -*- coding: utf-8 -*-
from python_facebook.sdk.const import VERSION
from python_facebook.sdk.const import DEFAULT_GRAPH_VERSION
from python_facebook.sdk.authentication.access_token import AccessToken
from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException
from python_facebook.sdk.file_upload.facebook_file import FacebookFile
from python_facebook.sdk.file_upload.facebook_video import FacebookVideo
from python_facebook.sdk.http.request_body_multipart import RequestBodyMultipart
from python_facebook.sdk.http.request_body_url_encoded import RequestBodyUrlEncoded
from python_facebook.sdk.url.facebook_url_manipulator import FacebookUrlManipulator

try:
    from simplejson import JSONDecodeError
except ImportError:
    class JSONDecodeError(ValueError):
        pass


class FacebookRequest(object):
    def __init__(self, app=None, access_token=None, method=None, endpoint=None, params=None, e_tag=None,
                 graph_version=None):
        self.set_app(app)
        self.set_access_token(access_token)
        self.set_method(method)
        self.set_endpoint(endpoint)
        self.reset_files()
        self.params = {}
        self.set_params(params or {})
        self.set_e_tag(e_tag)
        self.headers = self.get_default_headers()

        self.graph_version = graph_version or DEFAULT_GRAPH_VERSION

    def set_access_token(self, access_token=None):
        self.access_token = access_token
        if isinstance(access_token, AccessToken):
            self.access_token = access_token.get_value()
        return self

    def set_access_token_from_params(self, access_token):
        existing_access_token = self.get_access_token()
        if not existing_access_token:
            self.set_access_token(access_token)
        elif access_token != existing_access_token:
            raise FacebookSDKException('Access token mismatch. The access token provided in the FacebookRequest and '
                                       'the one provided in the URL or POST params do not match.')
        return self

    def get_access_token(self):
        return self.access_token

    def get_access_token_entity(self):
        return AccessToken(self.access_token) if self.access_token else None

    def set_app(self, app):
        self.app = app

    def get_app(self):
        return self.app

    def get_app_secret_proof(self):
        access_token_entity = self.get_access_token_entity()
        if not access_token_entity:
            return None
        return access_token_entity.get_app_secret_proof(self.app.get_secret())

    def validate_access_token(self):
        access_token = self.get_access_token()
        if not access_token:
            raise FacebookSDKException('You must provide an access token.')

    def set_method(self, method):
        self.method = method
        if self.method:
            self.method = self.method.upper()

    def get_method(self):
        return self.method

    def validate_method(self):
        if not self.method:
            raise FacebookSDKException('HTTP method not specified.')
        elif self.method not in ('GET', 'POST', 'DELETE'):
            raise FacebookSDKException('Invalid HTTP method specified.')

    def set_endpoint(self, endpoint):
        # Harvest the access token from the endpoint to keep things in sync
        params = FacebookUrlManipulator.get_params_as_array(endpoint)
        if params.get('access_token'):
            self.set_access_token_from_params(params['access_token'])

        # Clean the token & app secret proof from the endpoint.
        filter_params = ['access_token', 'appsecret_proof']
        self.endpoint = FacebookUrlManipulator.remove_params_from_url(endpoint, filter_params)
        return self

    def get_endpoint(self):
        return self.endpoint

    def get_headers(self):
        if self.e_tag:
            self.headers.update({
                'If-None-Match': self.e_tag
            })
        return self.headers

    def set_headers(self, headers):
        self.headers.update(headers)

    def set_e_tag(self, e_tag):
        self.e_tag = e_tag

    def set_params(self, params):
        if params.get('access_token'):
            self.set_access_token_from_params(params['access_token'])

        # Don't let these buggers slip in.
        params.pop('access_token', None)
        params.pop('appsecret_proof', None)

        # @TODO Refactor code above with this
        # params = self.sanitize_authentication_params(params)
        params = self.sanitize_file_params(params)
        self.dangerously_set_params(params)
        return self

    def dangerously_set_params(self, params):
        self.params.update(params)
        return self

    def sanitize_file_params(self, params):
        for key, value in params.items():
            if isinstance(value, FacebookFile):
                self.add_file(key, value)
                del params[key]
        return params

    def add_file(self, key, file):
        self.files.update({
            key: file
        })

    def reset_files(self):
        self.files = {}

    def get_files(self):
        return self.files

    def contains_file_uploads(self):
        return len(self.files)

    def contains_video_uploads(self):
        return any([isinstance(file, FacebookVideo) for file in self.files])

    def get_multipart_body(self):
        return RequestBodyMultipart(self.get_post_params(), self.files)

    def get_url_encoded_body(self):
        return RequestBodyUrlEncoded(self.get_post_params())

    def get_params(self):
        params = self.params
        access_token = self.get_access_token()
        if access_token:
            params.update({
                'access_token': access_token,
                'appsecret_proof': self.get_app_secret_proof()
            })
        return params

    def get_post_params(self):
        if self.get_method() == 'POST':
            return self.get_params()
        return None

    def get_graph_version(self):
        return self.graph_version

    def get_url(self):
        self.validate_method()
        url = '{}{}'.format(FacebookUrlManipulator.force_slash_prefix(self.graph_version),
                            FacebookUrlManipulator.force_slash_prefix(self.get_endpoint()))
        # return self.get_endpoint()
        if self.method != 'POST':
            params = self.get_params()
            url = FacebookUrlManipulator.append_params_to_url(url, params)
        return url

    @classmethod
    def get_default_headers(self):
        return {
            'User-Agent': 'fb-python-{}'.format(VERSION),
            'Accept-Encoding': '*',
        }
