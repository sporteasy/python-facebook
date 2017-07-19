from python_facebook.sdk.request import FacebookRequest
from python_facebook.sdk.response import FacebookResponse


class FacebookClient(object):
    # string Production Graph API URL.
    BASE_GRAPH_URL = 'https://graph.facebook.com'

    # string Graph API URL for video uploads.
    BASE_GRAPH_VIDEO_URL = 'https://graph-video.facebook.com'

    # string Beta Graph API URL.
    BASE_GRAPH_URL_BETA = 'https://graph.beta.facebook.com'

    # string Beta Graph API URL for video uploads
    BASE_GRAPH_VIDEO_URL_BETA = 'https://graph-video.beta.facebook.com'

    # int The timeout in seconds for a normal request.
    DEFAULT_REQUEST_TIMEOUT = 60

    # int The timeout in seconds for a request that contains file uploads.
    DEFAULT_FILE_UPLOAD_REQUEST_TIMEOUT = 3600

    # int The timeout in seconds for a request that contains video uploads.
    DEFAULT_VIDEO_UPLOAD_REQUEST_TIMEOUT = 7200

    def __init__(self, http_client_handler=None, enable_beta=False):
        self.http_client_handler = http_client_handler
        self.enable_beta_mode = enable_beta

        self.request_count = 0

    def set_http_client_handler(self, client_handler):
        self.http_client_handler = client_handler

    def get_http_client_handler(self):
        return self.http_client_handler

    def detect_http_client_handler(self):
        raise NotImplementedError

    def enable_beta_mode(self, beta_mode=True):
        self.enable_beta_mode = beta_mode

    def get_base_graph_url(self, post_to_video_url=False):
        if post_to_video_url:
            return self.BASE_GRAPH_VIDEO_URL_BETA if self.enable_beta_mode else self.BASE_GRAPH_VIDEO_URL

        return self.BASE_GRAPH_URL_BETA if self.enable_beta_mode else self.BASE_GRAPH_URL

    def prepare_request_message(self, request):
        post_to_video_url = request.contains_video_uploads()
        url = self.get_base_graph_url(post_to_video_url) + request.get_url()

        # If we're sending files they should be sent as multipart/form-data
        if request.contains_file_uploads():
            request_body = request.get_multipart_body()
            request.set_headers({
                'Content-Type': 'multipart/form-data; boundary=' + request_body.get_boundary()
            })
        else:
            request_body = request.get_url_encoded_body()
            request.set_headers({
                'Content-Type': 'application/x-www-form-urlencoded'
            })
        return url, request.get_method(), request.get_headers(), request.get_body()

    def send_request(self, request):
        if isinstance(request, FacebookRequest):
            request.validate_access_token()

        url, method, headers, body = self.prepare_request_message(request)

        # Since file uploads can take a while, we need to give more time for uploads
        timeout = self.DEFAULT_REQUEST_TIMEOUT
        if request.contains_file_uploads():
            timeout = self.DEFAULT_FILE_UPLOAD_REQUEST_TIMEOUT
        elif request.contains_video_uploads():
            timeout = self.DEFAULT_VIDEO_UPLOAD_REQUEST_TIMEOUT

        # Should throw `FacebookSDKException` exception on HTTP client error.
        # Don't catch to allow it to bubble up.
        raw_response = self.http_client_handler.send(url, method, body, headers, timeout)
        self.request_count += 1

        return_response = FacebookResponse(
            request,
            raw_response.get_body(),
            raw_response.get_http_response_code(),
            raw_response.get_headers()
        )

        if return_response.is_error():
            raise return_response.get_thrown_exception()

        return return_response
