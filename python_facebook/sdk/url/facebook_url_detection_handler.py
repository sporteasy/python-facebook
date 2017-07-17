class FacebookUrlDetectionHandler(object):

    def __init__(self, current_url=''):
        self.current_url = current_url

    def get_current_url(self):
        return self.current_url
