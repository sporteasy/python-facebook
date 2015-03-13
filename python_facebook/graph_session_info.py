# -*- coding: utf-8 -*-
from datetime import datetime

from python_facebook.graph_object import GraphObject


class GraphSessionInfo(GraphObject):

    def __init__(self, *args, **kwargs):
        self.app_id = None
        self.application = None
        self._expires_at = None
        self.is_valid = None
        self._issued_at = None
        self.scopes = []
        self.user_id = None

        super(GraphSessionInfo, self).__init__(*args, **kwargs)

    @property
    def expires_at(self):
        if not self._expires_at:
            return None
        return datetime.fromtimestamp(self._expires_at)

    @expires_at.setter
    def expires_at(self, value):
        self._expires_at = value

    @property
    def issued_at(self):
        if not self._issued_at:
            return None
        return datetime.fromtimestamp(self._issued_at)

    @issued_at.setter
    def issued_at(self, value):
        self._issued_at = value
