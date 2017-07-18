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
        return [
            url,
            request.get_method(),
            request.get_headers(),
            request.get_body()
        ]

    def send_request(self, request):
        raise NotImplementedError
