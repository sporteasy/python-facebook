from python_facebook.sdk.http_clients. \
    facebook_requests_http_client import FacebookRequestsHttpClient


class HttpClientsFactory(object):
    @classmethod
    def create_http_client(cls, handler=None):
        if handler:
            return handler

        return FacebookRequestsHttpClient()
