from python_facebook.sdk.persistent_data.facebook_memory_persistent_data_handler import \
    FacebookMemoryPersistentDataHandler


class PersistentDataFactory(object):

    @classmethod
    def create_persistent_data_handler(cls, handler=None):
        if handler:
            return handler

        return FacebookMemoryPersistentDataHandler()
