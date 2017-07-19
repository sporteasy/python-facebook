import unittest

from python_facebook.sdk.graph_nodes.graph_node import GraphNode


class GraphNodeTestCase(unittest.TestCase):

    def test_an_empty_base_graph_node_can_instantiate(self):
        graph_node = GraphNode()
        backing_data = graph_node.as_array()

        self.assertEqual({}, backing_data)

    def test_a_graph_node_can_instantiate_with_data(self):
        graph_node = GraphNode({'foo': 'bar'})
        backing_data = graph_node.as_array()

        self.assertEqual({'foo': 'bar'}, backing_data)

    def test_dates_that_should_be_cast_as_date_time_objects_are_detected(self):
        graph_node = GraphNode()

        # should pass
        should_pass = graph_node.is_iso8601_date_string('1985-10-26T01:21:00+0000')
        self.assertTrue(should_pass, 'Expected the valid ISO 8601 formatted date from Back To The Future to pass.')

        should_pass = graph_node.is_iso8601_date_string('1999-12-31')
        self.assertTrue(should_pass, 'Expected the valid ISO 8601 formatted date to party like it\'s 1999.')

        should_pass = graph_node.is_iso8601_date_string('2009-05-19T14:39Z')
        self.assertTrue(should_pass, 'Expected the valid ISO 8601 formatted date to pass.')

        should_pass = graph_node.is_iso8601_date_string('2014-W36')
        self.assertTrue(should_pass, 'Expected the valid ISO 8601 formatted date to pass.')

        should_pass = graph_node.is_iso8601_date_string('2014-W06')
        self.assertTrue(should_pass, 'Expected the valid ISO 8601 formatted date to pass.')

        should_pass = graph_node.is_iso8601_date_string('2014-W51')
        self.assertTrue(should_pass, 'Expected the valid ISO 8601 formatted date to pass.')

        # should fail
        should_fail = graph_node.is_iso8601_date_string('2009-05-19T14a39r')
        self.assertFalse(should_fail, 'Expected the invalid ISO 8601 format to fail.')

        should_fail = graph_node.is_iso8601_date_string('foo_time')
        self.assertFalse(should_fail, 'Expected the invalid ISO 8601 format to fail.')

        should_fail = graph_node.is_iso8601_date_string('2014-W53')
        self.assertFalse(should_fail, 'Expected the invalid ISO 8601 format to fail.')

        should_fail = graph_node.is_iso8601_date_string('2014-W3')
        self.assertFalse(should_fail, 'Expected the invalid ISO 8601 format to fail.')

    def test_a_time_stamp_can_be_converted_to_adate_time_object(self):
        pass
