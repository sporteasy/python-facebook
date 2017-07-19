class FacebookSDKException(Exception):
    def __init__(self, message, code=None):
        self.message = message
        self.code = code
        super(FacebookSDKException, self).__init__(message)
