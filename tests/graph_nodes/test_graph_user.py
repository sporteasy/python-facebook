import mock
import unittest

from datetime import datetime

from python_facebook.sdk.graph_nodes.birthday import Birthday
from python_facebook.sdk.graph_nodes.graph_node_factory import GraphNodeFactory


class GraphUserTestCase(unittest.TestCase):

    def setUp(self):
        self.response_mock = None

    def test_dates_get_cast_to_date_time(self):
        data_from_graph = {
            'updated_time': '2016-04-26 13:22:05'
        }

        # todo mock

        factory = GraphNodeFactory(self.response_mock)
        graph_node = factory.make_graph_user()

        updated_time = graph_node.get_field('updated_time')

        self.assertIsInstance(updated_time, datetime)

    def test_birthdays_get_cast_to_birthday(self):
        data_from_graph = {
            'birthday': '1984/01/01'
        }

        # todo mock
        factory = GraphNodeFactory(self.response_mock)
        graph_node = factory.make_graph_user()

        birthday = graph_node.get_birthday()

        self.assertIsInstance(birthday, Birthday)
        self.assertTrue(birthday.has_date)
        self.assertTrue(birthday.has_year)
        self.assertEqual('1984/01/01', birthday.format('%Y/%m/%d'))

