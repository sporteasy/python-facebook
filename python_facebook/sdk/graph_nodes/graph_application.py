from python_facebook.sdk.graph_nodes.graph_node import GraphNode


class GraphApplication(GraphNode):

    def get_id(self):
        self.get_field('id')
