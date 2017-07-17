from python_facebook.sdk.exceptions.facebook_sdk_exception import FacebookSDKException


class FacebookResponseException(FacebookSDKException):

    @staticmethod
    def create(response):
        data = response.get_decoded_body()
