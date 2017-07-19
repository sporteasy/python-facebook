# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from python_facebook.sdk.utils import JSONEncoder


class BaseCollection(object):
    def __init__(self, items=None):
        if not items:
            items = {}
        self.items = items

    def __eq__(self, other):
        return self.as_json() == other.as_json()

    def __repr__(self):
        return self.items

    def get_field(self, name, default=None):
        """
        Gets the value of a field from the Graph node.
        """
        return self.items.get(name, default)

    def set_field(self, name, value):
        self.items[name] = value

    def get_field_names(self):
        """
        Returns a list of all fields set on the object.
        """
        return self.items.keys()

    def all(self):
        return self.items

    def as_array(self):
        if isinstance(self.items, dict):
            def get_array_value(value):
                return value.as_array() if isinstance(value, BaseCollection) \
                    else value

            return {key: get_array_value(value) for key, value in
                    self.items.items()}
        else:
            return self.items

    def map(self, func):
        raise NotImplementedError

    def as_json(self, **kwargs):
        return JSONEncoder().encode(self.items)

    def count(self):
        return len(self.items)

    def get_iterator(self):
        raise NotImplementedError
