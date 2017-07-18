import json


class BaseCollection(object):

    def __init__(self, items=None):
        if not items:
            items = {}
        self.items = items

    def get_field(self, name, default=None):
        """
        Gets the value of a field from the Graph node.
        """
        return self.items.get(name, default)

    def get_field_names(self):
        """
        Returns a list of all fields set on the object.
        """
        return self.items.keys()

    def all(self):
        return self.items

    def as_array(self):
        def get_array_value(value):
            return value.as_array() if isinstance(value, BaseCollection) else value

        return {key: get_array_value(value) for key, value in self.items.items()}

    def map(self, func):
        raise NotImplementedError

    def as_json(self, **kwargs):
        return json.dumps(self.items, **kwargs)

    def count(self):
        return len(self.items)

    def get_iterator(self):
        raise NotImplementedError
