# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from python_facebook.sdk.graph_nodes.graph_node import GraphNode


class MyFooGraphNode(GraphNode):
    graph_object_map = {
        'foo_object': 'tests.fixtures.my_foo_sub_class_graph_node.'
                      'MyFooSubClassGraphNode',
    }
