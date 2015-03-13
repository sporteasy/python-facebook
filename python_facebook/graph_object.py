# -*- coding: utf-8 -*-


class GraphObject(object):
    """
    Creates a GraphObject using the data provided
    """

    def __init__(self, *args, **kwargs):
        self.backing_data = kwargs

        if self.backing_data.get('data') and len(self.backing_data) == 1:
            self.backing_data = self.backing_data['data']

        for key, value in self.backing_data.items():
            setattr(self, key, value)
