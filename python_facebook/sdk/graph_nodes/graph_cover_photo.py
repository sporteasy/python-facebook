from python_facebook.sdk.graph_nodes.graph_node import GraphNode


class GraphCoverPhoto(GraphNode):

    def get_id(self):
        return self.get_field('id')

    def get_source(self):
        return self.get_field('source')

    def get_offset_x(self):
        return self.get_field('offset_x')

    def get_offset_y(self):
        return self.get_field('offset_y')
