import json
from collections import OrderedDict
from datetime import datetime
from time import mktime

import dateutil

from tests import PythonFacebookTestCase

from python_facebook.sdk.graph_nodes.graph_node import GraphNode

FORMAT_RFC1036 = '%a, %d %b %y %H:%M:%S %z'


class GraphNodeTestCase(PythonFacebookTestCase):
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
        should_pass = graph_node.is_iso8601_date_string(
            '1985-10-26T01:21:00+0000')
        self.assertTrue(should_pass,
                        'Expected the valid ISO 8601 formatted date from '
                        'Back To The Future to pass.')

        should_pass = graph_node.is_iso8601_date_string('1999-12-31')
        self.assertTrue(should_pass,
                        'Expected the valid ISO 8601 formatted date to '
                        'party like it\'s 1999.')

        should_pass = graph_node.is_iso8601_date_string('2009-05-19T14:39Z')
        self.assertTrue(should_pass,
                        'Expected the valid ISO 8601 formatted date to pass.')

        should_pass = graph_node.is_iso8601_date_string('2014-W36')
        self.assertTrue(should_pass,
                        'Expected the valid ISO 8601 formatted date to pass.')

        should_pass = graph_node.is_iso8601_date_string('2014-W06')
        self.assertTrue(should_pass,
                        'Expected the valid ISO 8601 formatted date to pass.')

        should_pass = graph_node.is_iso8601_date_string('2014-W51')
        self.assertTrue(should_pass,
                        'Expected the valid ISO 8601 formatted date to pass.')

        # should fail
        should_fail = graph_node.is_iso8601_date_string('2009-05-19T14a39r')
        self.assertFalse(should_fail,
                         'Expected the invalid ISO 8601 format to fail.')

        should_fail = graph_node.is_iso8601_date_string('foo_time')
        self.assertFalse(should_fail,
                         'Expected the invalid ISO 8601 format to fail.')

        should_fail = graph_node.is_iso8601_date_string('2014-W53')
        self.assertFalse(should_fail,
                         'Expected the invalid ISO 8601 format to fail.')

        should_fail = graph_node.is_iso8601_date_string('2014-W3')
        self.assertFalse(should_fail,
                         'Expected the invalid ISO 8601 format to fail.')

    def test_a_time_stamp_can_be_converted_to_adate_time_object(self):
        someTimeStampFromGraph = 1405547020
        graphNode = GraphNode()
        dateTime = graphNode.cast_to_datetime(someTimeStampFromGraph)
        prettyDate = dateTime.strftime(FORMAT_RFC1036)
        timeStamp = mktime(dateTime.timetuple())
        self.assertIsInstance(dateTime, datetime)
        self.assertEqual('Wed, 16 Jul 14 23:43:40 +0200', prettyDate)
        self.assertEqual(1405547020, timeStamp)

    def testAGraphDateStringCanBeConvertedToADateTimeObject(self):
        someDateStringFromGraph = '2014-07-15T03:44:53+0000'
        graphNode = GraphNode()
        dateTime = graphNode.cast_to_datetime(someDateStringFromGraph)
        prettyDate = dateTime.strftime(FORMAT_RFC1036)
        timeStamp = mktime(dateTime.timetuple())
        self.assertIsInstance(dateTime, datetime)
        self.assertEqual('Tue, 15 Jul 14 03:44:53 +0000', prettyDate)
        # TODO python timestamp does not care about TZ it seems
        self.assertEqual(1405395893, timeStamp + 3600)

    def testUncastingAGraphNodeWillUncastTheDateTimeObject(self):
        collectionOne = GraphNode(['foo', 'bar'])
        collectionTwo = GraphNode({
            'id': '123',
            'date': dateutil.parser.parse('2014-07-15T03:44:53+0000'),
            'some_collection': collectionOne,
        })
        uncastArray = collectionTwo.uncast_items()
        self.assertEqual({
            'id': '123',
            'date': '2014-07-15T03:44:53+0000',
            'some_collection': ['foo', 'bar'],
        }, uncastArray)

    def testGettingGraphNodeAsAnArrayWillNotUncastTheDateTimeObject(self):
        collection = GraphNode({
            'id': '123',
            'date': dateutil.parser.parse('2014-07-15T03:44:53+0000'),
        })
        collectionAsArray = collection.as_array()
        self.assertIsInstance(collectionAsArray['date'], datetime)

    def testReturningACollectionAsJasonWillSafelyRepresentDateTimes(self):
        collection = GraphNode(OrderedDict({
            'date': dateutil.parser.parse('2014-07-15T03:44:53+0000'),
            'id': '123',
        }))
        collectionAsString = collection.as_json()

        expected = '{"date": "2014-07-15T03:44:53+0000", "id": "123"}'
        self.assertEqual(len(expected), len(collectionAsString))
        self.assertEqual(json.loads(expected), json.loads(collectionAsString))
