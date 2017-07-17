import datetime
import json
import re

from python_facebook.sdk.graph_nodes.base_graph_collection import BaseCollection
from python_facebook.sdk.graph_nodes.birthday import Birthday


class GraphNode(BaseCollection):
    graph_object_map = {}

    def __init__(self, data=None):
        if data is None:
            data = {}

        super(GraphNode, self).__init__(self.cast_items(data))

    def cast_items(self, data):
        items = {}
        for key, val in data.items():
            if (self.should_cast_as_datetime(key)) and \
                    (isinstance(val, int) or self.is_iso8601_date_string(val)):
                items[key] = self.cast_to_datetime(val)
            elif key == 'birthday':
                items[key] = self.cast_to_birthday(val)
            else:
                items[key] = val
        return items

    def uncast_items(self):
        # Todo
        raise NotImplementedError

    def as_json(self, **kwargs):
        """
        Get the collection of items as JSON.
        """
        return json.dumps(self.uncast_items(), **kwargs)

    def is_iso8601_date_string(self, string):
        """
        Detects an ISO 8601 formatted string.

        @see https://developers.facebook.com/docs/graph-api/using-graph-api/#readmodifiers
        @see http://www.cl.cam.ac.uk/~mgk25/iso-time.html
        @see http://en.wikipedia.org/wiki/ISO_8601
        """
        # This insane regex was yoinked from here:
        # http://www.pelagodesign.com/blog/2009/05/20/iso-8601-date-validation-that-doesnt-suck/
        # ...and I'm all like:
        # http://thecodinglove.com/post/95378251969/when-code-works-and-i-dont-know-why
        crazyInsaneRegexThatSomehowDetectsIso8601 = '/^([\+-]?\d{4}(?!\d{2}\b))' \
            '((-?)((0[1-9]|1[0-2])(\3([12]\d|0[1-9]|3[01]))?' \
            '|W([0-4]\d|5[0-2])(-?[1-7])?|(00[1-9]|0[1-9]\d' \
            '|[12]\d{2}|3([0-5]\d|6[1-6])))([T\s]((([01]\d|2[0-3])' \
            '((:?)[0-5]\d)?|24\:?00)([\.,]\d+(?!:))?)?(\17[0-5]\d' \
            '([\.,]\d+)?)?([zZ]|([\+-])([01]\d|2[0-3]):?([0-5]\d)?)?)?)?$/'
        return re.match(crazyInsaneRegexThatSomehowDetectsIso8601, string) == 1

    def should_cast_as_datetime(self, key):
        """
        Determines if a value from Graph should be cast to DateTime.
        """
        return key in [
            'created_time',
            'updated_time',
            'start_time',
            'end_time',
            'backdated_time',
            'issued_at',
            'expires_at',
            'publish_time'
        ]

    def cast_to_datetime(self, value):
        """
        Casts a date value from Graph to DateTime.
        """
        if isinstance(value, int):
            dt = datetime.datetime.fromtimestamp(value / 1e3)
        else:
            dt = datetime.datetime.strptime(value, 'Y%-%m-%d')
        return dt

    def cast_to_birthday(self, value):
        """
        Casts a birthday value from Graph to Birthday
        """
        return Birthday(value)

    @classmethod
    def get_object_map(cls):
        return cls.graph_object_map

