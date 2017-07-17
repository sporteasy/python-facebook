# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class FacebookResumableUploader(object):
    def __init__(self, *args, **kwargs):
        pass

    def start(self, endpoint, file):
        pass

    def transfer(self, endpoint, chunk, allow_to_throw=False):
        pass

    def finish(self, endpoint, upload_session_id, metadata=None):
        pass
