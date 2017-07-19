from python_facebook.sdk.graph_nodes.graph_node import GraphNode


class GraphPage(GraphNode):
    graph_object_map = {
        'best_page': '.graph_nodes.GraphPage',
        'global_brand_parent_page': '.graph_nodes.GraphPage',
        'location': '.graph_nodes.GraphLocation',
        'cover': '.graph_nodes.GraphCoverPhoto',
        'picture': '.graph_nodes.GraphPicture'
    }

    def get_id(self):
        return self.get_field('id')

    def get_category(self):
        return self.get_field('category')

    def get_name(self):
        return self.get_field('name')

    def get_best_page(self):
        return self.get_field('best_page')

    def get_global_brand_parent_page(self):
        return self.get_field('global_brand_parent_page')

    def get_location(self):
        return self.get_field('location')

    def get_cover(self):
        return self.get_field('cover')

    def get_picture(self):
        return self.get_field('picture')

    def get_access_token(self):
        return self.get_field('access_token')

    def get_perms(self):
        return self.get_field('perms')
