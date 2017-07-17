class FacebookMemoryPersistentDataHandler(object):

    def __init__(self):
        self.session_data = {}

    def get(self, key):
        return self.session_data.get(key)

    def set(self, key, value):
        self.session_data[key] = value
