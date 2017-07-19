import os

from python_facebook.sdk.const import VERSION
from python_facebook.sdk.const import DEFAULT_GRAPH_VERSION
from python_facebook.sdk.authentication.access_token import AccessToken
from python_facebook.sdk.authentication.oauth2_client import OAuth2Client
from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException
from python_facebook.sdk.facebook_app import FacebookApp
from python_facebook.sdk.facebook_client import FacebookClient
from python_facebook.sdk.file_upload.facebook_file import FacebookFile
from python_facebook.sdk.file_upload.facebook_video import FacebookVideo
from python_facebook.sdk.helpers.facebook_redirect_login_helper import FacebookRedirectLoginHelper
from python_facebook.sdk.http_clients.http_clients_factory import HttpClientsFactory
from python_facebook.sdk.persistent_data.persistent_data_factory import PersistentDataFactory
from python_facebook.sdk.pseudo_random_string.pseudo_random_string_generator_factory import \
    PseudoRandomStringGeneratorFactory
from python_facebook.sdk.request import FacebookRequest
from python_facebook.sdk.url.facebook_url_detection_handler import FacebookUrlDetectionHandler


class Facebook(object):

    # string version of this python FB sdk implementation
    VERSION = VERSION

    # string Default Graph API version for requests.
    DEFAULT_GRAPH_VERSION = DEFAULT_GRAPH_VERSION

    # string The name of the environment variable that contains the app ID.
    APP_ID_ENV_NAME = 'FACEBOOK_APP_ID'

    # string The name of the environment variable that contains the app secret.
    APP_SECRET_ENV_NAME = 'FACEBOOK_APP_SECRET'

    def __init__(self, override_config=None):
        self.oauth2_client = None
        self.last_response = None
        self.url_detection_handler = None
        self.default_access_token = None

        config = {
            'app_id': os.environ.get(self.APP_ID_ENV_NAME, None),
            'app_secret': os.environ.get(self.APP_SECRET_ENV_NAME, None),
            'default_graph_version': self.DEFAULT_GRAPH_VERSION,
            'enable_beta_mode': False,
            'http_client_handler': None,
            'persistent_data_handler': None,
            'pseudo_random_string_generator': None,
            'url_detection_handler': None
        }

        if override_config:
            config.update(override_config)

        if not config['app_id']:
            raise FacebookSDKException('Required "app_id" key not supplied in config and could not find '
                                       'fallback environment variable "' + self.APP_ID_ENV_NAME + '"')

        if not config['app_secret']:
            raise FacebookSDKException('Required "app_secret" key not supplied in config and could not find '
                                       'fallback environment variable "' + self.APP_SECRET_ENV_NAME + '"')

        self.app = FacebookApp(
            config['app_id'],
            config['app_secret']
        )
        self.client = FacebookClient(
            HttpClientsFactory.create_http_client(config['http_client_handler']),
            config['enable_beta_mode']
        )
        self.prsg = PseudoRandomStringGeneratorFactory.create_pseudo_random_string_generator(
            config['pseudo_random_string_generator']
        )
        self.set_url_detection_handler(config['url_detection_handler'] or FacebookUrlDetectionHandler())
        self.persistent_data_handler = PersistentDataFactory.create_persistent_data_handler(
            config['persistent_data_handler']
        )

        if config.get('default_access_token'):
            self.set_default_access_token(config['default_access_token'])

        # @todo v6: Throw an InvalidArgumentException if "default_graph_version" is not set
        self.default_graph_version = config['default_graph_version']

    def get_app(self):
        return self.app

    def get_client(self):
        return self.client

    def get_oauth2_client(self):
        if not isinstance(self.oauth2_client, OAuth2Client):
            self.oauth2_client = OAuth2Client(self.app, self.client, self.default_graph_version)
        return self.oauth2_client

    def get_last_response(self):
        return self.last_response

    def get_url_detection_handler(self):
        return self.url_detection_handler

    def set_url_detection_handler(self, handler):
        self.url_detection_handler = handler

    def get_default_access_token(self):
        return self.default_access_token

    def set_default_access_token(self, access_token):
        if isinstance(access_token, str):
            self.default_access_token = AccessToken(access_token)
            return
        elif isinstance(access_token, AccessToken):
            self.default_access_token = access_token
            return
        raise ValueError('The default access token must be of type "string" or AccessToken')

    def get_default_graph_version(self):
        return self.default_graph_version

    def get_redirect_login_helper(self):
        return FacebookRedirectLoginHelper(
            self.get_oauth2_client(),
            self.persistent_data_handler,
            self.url_detection_handler,
            self.prsg
        )

    def get_javascript_helper(self):
        raise NotImplementedError

    def get_cancas_helper(self):
        raise NotImplementedError

    def get_page_tab_helper(self):
        raise NotImplementedError

    def get(self, endpoint, access_token=None, etag=None, graph_version=None):
        return self.send_request(
            'GET',
            endpoint,
            None,
            access_token,
            etag,
            graph_version
        )

    def post(self, endpoint, params=None, access_token=None, etag=None, graph_version=None):
        return self.send_request(
            'POST',
            endpoint,
            params,
            access_token,
            etag,
            graph_version
        )

    def delete(self, endpoint, params=None, access_token=None, etag=None, graph_version=None):
        return self.send_request(
            'DELETE',
            endpoint,
            params,
            access_token,
            etag,
            graph_version
        )

    def next_page(self, graph_edge):
        raise NotImplementedError

    def previous_page(self, graph_edge):
        raise NotImplementedError

    def get_pagincation_results(self, graph_edge, direction):
        raise NotImplementedError

    def send_request(self, method, endpoint, params=None, access_token=None, etag=None, graph_version=None):
        access_token = access_token or self.default_access_token
        graph_version = graph_version or self.default_graph_version
        request = self.request(method, endpoint, params, access_token, etag, graph_version)

        self.last_response = self.client.send_request(request)
        return self.last_response

    def send_batch_request(self, requests, access_token=None, graph_version=None):
        # access_token = access_token or self.default_access_token
        # graph_version = graph_version or self.default_graph_version
        # batch_request = FacebookBatchRequest(
        #     self.app,
        #     requests,
        #     access_token,
        #     graph_version
        # )
        #
        # self.last_response = self.client.send_batch_request(batch_request)
        # return self.last_response
        raise NotImplementedError

    def new_batch_request(self, access_token=None, graph_version=None):
        access_token = access_token or self.default_access_token
        graph_version = graph_version or self.default_graph_version

        raise NotImplementedError

    def request(self, method, endpoint, params=None, access_token=None, etag=None, graph_version=None):
        access_token = access_token or self.default_access_token
        graph_version = graph_version or self.default_graph_version

        return FacebookRequest(
            self.app,
            access_token,
            method,
            endpoint,
            params,
            etag,
            graph_version
        )

    def file_to_upload(self, path_to_file):
        return FacebookFile(path_to_file)

    def video_to_upload(self, path_to_file):
        return FacebookVideo(path_to_file)

    def upload_video(self, target, path_to_file, metadata=None, access_token=None, max_transfer_tries=5,
                     graph_version=None):
        raise NotImplementedError

    def max_tries_transfer(self, uploader, endpoint, chunk, retry_countdown):
        raise NotImplementedError
