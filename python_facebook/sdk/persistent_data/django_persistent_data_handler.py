class DjangoPersistentDataHandler(object):

    def __init__(self, session):
        self.session = session

    def get(self, key):
        return self.session.get(key)

    def set(self, key, value):
        self.session[key] = value
