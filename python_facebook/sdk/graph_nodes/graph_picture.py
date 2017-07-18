from python_facebook.sdk.graph_nodes.graph_node import GraphNode


class GraphPicture(GraphNode):

    def is_silhouette(self):
        return self.get_field('is_silhouette')

    def get_url(self):
        return self.get_field('url')

    def get_width(self):
        return self.get_field('width')

    def get_height(self):
        return self.get_field('height')
