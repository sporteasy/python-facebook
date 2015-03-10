# -*- coding: utf-8 -*-


class GraphObject(object):

    def __init__(self, *args, **kwargs):
        self.backing_data = kwargs
        self.__dict__.update(kwargs)
