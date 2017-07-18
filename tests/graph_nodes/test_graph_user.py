import mock
import unittest

from datetime import datetime

from python_facebook.sdk.graph_nodes import GraphUser, GraphPicture
from python_facebook.sdk.graph_nodes.birthday import Birthday
from python_facebook.sdk.graph_nodes.graph_node_factory import GraphNodeFactory
from python_facebook.sdk.graph_nodes.graph_page import GraphPage
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

    def test_birthday_cast_handles_date_without_year(self):
        data_from_graph = {
            'birthday': '03/21'
        }
        response_mock = mock.Mock(spec=FacebookResponse)
        response_mock.get_decoded_body.return_value = data_from_graph

        factory = GraphNodeFactory(response_mock)
        graph_node = factory.make_graph_user()

        birthday = graph_node.get_birthday()

        self.assertIsInstance(birthday, Birthday)
        self.assertTrue(birthday.has_date)
        self.assertFalse(birthday.has_year)
        self.assertEqual('03/21', birthday.format('%m/%d'))

    def test_birthday_cast_handles_year_without_date(self):
        data_from_graph = {
            'birthday': '1984'
        }
        response_mock = mock.Mock(spec=FacebookResponse)
        response_mock.get_decoded_body.return_value = data_from_graph

        factory = GraphNodeFactory(response_mock)
        graph_node = factory.make_graph_user()

        birthday = graph_node.get_birthday()

        self.assertIsInstance(birthday, Birthday)
        self.assertTrue(birthday.has_year)
        self.assertFalse(birthday.has_date)
        self.assertEqual('1984', birthday.format('%Y'))

    def test_page_properties_will_get_cast_as_graph_page_objects(self):
        data_from_graph = {
            'id': '123',
            'name': 'Foo User',
            'hometown': {
                'id': '1',
                'name': 'Foo Place'
            },
            'location': {
                'id': '2',
                'name': 'Bar Place'
            }
        }
        response_mock = mock.Mock(spec=FacebookResponse)
        response_mock.get_decoded_body.return_value = data_from_graph

        factory = GraphNodeFactory(response_mock)
        graph_node = factory.make_graph_user()

        hometown = graph_node.get_hometown()
        location = graph_node.get_location()

        self.assertIsInstance(hometown, GraphPage)
        self.assertIsInstance(location, GraphPage)

    def test_user_properties_will_get_cast_as_graph_user_objects(self):
        data_from_graph = {
            'id': '123',
            'name': 'Foo User',
            'significant_other': {
                'id': '1337',
                'name': 'Bar User'
            }
        }
        response_mock = mock.Mock(spec=FacebookResponse)
        response_mock.get_decoded_body.return_value = data_from_graph

        factory = GraphNodeFactory(response_mock)
        graph_node = factory.make_graph_user()

        significant_other = graph_node.get_significant_other()

        self.assertIsInstance(significant_other, GraphUser)

    def test_picture_properties_will_get_cast_as_graph_picture_objects(self):
        data_from_graph = {
            'id': '123',
            'name': 'Foo User',
            'picture': {
                'is_silhouette': True,
                'url': 'http://foo.bar',
                'width': 200,
                'height': 200
            }
        }
        response_mock = mock.Mock(spec=FacebookResponse)
        response_mock.get_decoded_body.return_value = data_from_graph

        factory = GraphNodeFactory(response_mock)
        graph_node = factory.make_graph_user()

        picture = graph_node.get_picture()

        self.assertIsInstance(picture, GraphPicture)
        self.assertTrue(picture.is_silhouette())
        self.assertEqual(200, picture.get_width())
        self.assertEqual(200, picture.get_height())
        self.assertEqual('http://foo.bar', picture.get_url())
