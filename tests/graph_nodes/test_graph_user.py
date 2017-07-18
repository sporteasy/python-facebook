import mock
import unittest

from datetime import datetime

from python_facebook.sdk.graph_nodes.birthday import Birthday
from python_facebook.sdk.graph_nodes.graph_node_factory import GraphNodeFactory
from python_facebook.sdk.response import FacebookResponse


class GraphUserTestCase(unittest.TestCase):

    def test_dates_get_cast_to_date_time(self):
        data_from_graph = {
            'updated_time': '2016-04-26 13:22:05'
        }
        response_mock = mock.Mock(spec=FacebookResponse)
        response_mock.get_decoded_body.return_value = data_from_graph

        factory = GraphNodeFactory(response_mock)
        graph_node = factory.make_graph_user()

        updated_time = graph_node.get_field('updated_time')

        self.assertIsInstance(updated_time, datetime)

    def test_birthdays_get_cast_to_birthday(self):
        data_from_graph = {
            'birthday': '1984/01/01'
        }
        response_mock = mock.Mock(spec=FacebookResponse)
        response_mock.get_decoded_body.return_value = data_from_graph

        factory = GraphNodeFactory(response_mock)
        graph_node = factory.make_graph_user()

        birthday = graph_node.get_birthday()

        self.assertIsInstance(birthday, Birthday)
        self.assertTrue(birthday.has_date)
        self.assertTrue(birthday.has_year)
        self.assertEqual('1984/01/01', birthday.format('%Y/%m/%d'))

