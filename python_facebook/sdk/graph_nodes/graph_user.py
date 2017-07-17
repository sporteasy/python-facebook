# -*- coding: utf-8 -*-
from python_facebook.sdk.graph_nodes.graph_node import GraphNode


class GraphUser(GraphNode):
    graph_object_map = {
        'hometown': 'graph_nodes.GraphPage',
        'location': 'graph_nodes.GraphPage',
        'significant_other': 'graph_nodes.GraphUser',
        'picture': 'graph_nodes.GraphPicture'
    }

    def get_id(self):
        return self.get_field('id')

    def get_name(self):
        return self.get_field('name')

    def get_first_name(self):
        return self.get_field('first_name')

    def get_middle_name(self):
        return self.get_field('middle_name')

    def get_last_name(self):
        return self.get_field('last_name')

    def get_email(self):
        return self.get_field('email')

    def get_gender(self):
        return self.get_field('gender')

    def get_link(self):
        return self.get_field('link')

    def get_birthday(self):
        return self.get_field('birthday')

    def get_location(self):
        return self.get_field('location')

    def get_hometown(self):
        return self.get_field('hometown')

    def get_significant_other(self):
        return self.get_field('significant_other')

    def get_picture(self):
        return self.get_field('picture')
