from python_facebook.sdk.graph_nodes.graph_node import GraphNode


class GraphLocation(GraphNode):

    def get_street(self):
        return self.get_field('street')

    def get_city(self):
        return self.get_field('city')

    def get_state(self):
        return self.get_field('state')

    def get_country(self):
        return self.get_field('country')

    def get_zip(self):
        return self.get_field('zip')

    def get_latitude(self):
        return self.get_field('latitude')

    def get_longitude(self):
        return self.get_field('longitude')
