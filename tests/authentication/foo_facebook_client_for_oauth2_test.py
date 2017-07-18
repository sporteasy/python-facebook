from python_facebook.sdk.response import FacebookResponse


class FooFacebookClientForOAuth2Test(object):

    def set_metadata_response(self):
        self.response = '{"data":{"user_id":"444"}}'

    def set_access_token_response(self):
        self.response = '{"access_token":"my_access_token","expires":"1422115200"}'

    def set_code_response(self):
        self.response = '{"code":"my_neat_code"}'

    def send_request(self, request):
        return FacebookResponse(
            request,
            self.response,
            200,
            []
        )
