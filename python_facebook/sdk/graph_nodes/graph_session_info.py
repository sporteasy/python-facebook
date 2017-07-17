# -*- coding: utf-8 -*-
from python_facebook.sdk.graph_nodes.graph_node import GraphNode


class GraphSessionInfo(GraphNode):

    def get_app_id(self):
        return self.get_field('app_id')

    def get_application(self):
        return self.get_field('application')

    def get_expires_at(self):
        return self.get_field('expires_at')

    def get_is_valid(self):
        return self.get_field('is_valid')

    def get_issued_at(self):
        return self.get_field('issued_at')

    def get_scopes(self):
        return self.get_field('scopes')

    def get_user_id(self):
        return self.get_field('user_id')
