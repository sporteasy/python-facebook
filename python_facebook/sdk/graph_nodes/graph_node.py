import datetime
import json
import re
from tzlocal import get_localzone

from dateutil.parser import parse as date_parse

from python_facebook.sdk.graph_nodes.base_graph_collection import BaseCollection
from python_facebook.sdk.graph_nodes.birthday import Birthday
from python_facebook.sdk.utils import JSONEncoder

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

class GraphNode(BaseCollection):
    graph_object_map = {}

    def __init__(self, data=None):
        if data is None:
            data = {}

        super(GraphNode, self).__init__(self.cast_items(data))

    def __getitem__(self, item):
        return self.get_field(item)

    def cast_items(self, data):
        if isinstance(data, dict):
            return self._cast_dict(data)
        else:
            return self._cast_list(data)

    def _cast_dict(self, data):
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

    def _cast_list(self, data):
        return data

    def uncast_items(self):
        items = self.as_array()
        return {k: v.strftime(DATE_FORMAT) if isinstance(v, datetime.datetime) else v for k, v in items.items()}

    def as_json(self, **kwargs):
        """
        Get the collection of items as JSON.
        """
        return JSONEncoder().encode(self.uncast_items())

    def is_iso8601_date_string(self, string):
        """
        Detects an ISO 8601 formatted string.

        @see https://developers.facebook.com/docs/graph-api/using-graph-api/#readmodifiers
        @see http://www.cl.cam.ac.uk/~mgk25/iso-time.html
        @see http://en.wikipedia.org/wiki/ISO_8601
        """
        # Using a python shortcut with dateutil
        # Replace the insane PHP regex by a try/except with dateutil.parse
        # Difference with the original version: It will accept ISO 8601, RFC 3339, and more
        try:
            date_parse(string)
            return True
        except ValueError:
            # date_parse raises for dates like 2014-W36, so let's give him another chance
            pattern = '^\d{4}\-W([0-4][0-9]|5[0-2])$'
            return re.match(pattern, string) is not None

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
            div = 1e3 if len(str(value)) == 13 else 1   # if len is 13, we got microseconds
            dt = datetime.datetime.fromtimestamp(value / div)
        else:
            dt = date_parse(value)
        if dt.tzinfo is None:
            dt = get_localzone().localize(dt)
        return dt

    def cast_to_birthday(self, value):
        """
        Casts a birthday value from Graph to Birthday
        """
        return Birthday(value)

    @classmethod
    def get_object_map(cls):
        return cls.graph_object_map

