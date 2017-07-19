import mock

from datetime import datetime

from tests import PythonFacebookTestCase
from python_facebook.sdk.graph_nodes.graph_node_factory import GraphNodeFactory
from python_facebook.sdk.response import FacebookResponse


class GraphSessionInfoTestCase(PythonFacebookTestCase):

    def test_dates_get_cast_to_date_time(self):
        data_from_graph = {
            'expires_at': 123,
            'issued_at': 1337
        }

        response_mock = mock.Mock(spec=FacebookResponse)
        response_mock.get_decoded_body.return_value = data_from_graph

        factory = GraphNodeFactory(response_mock)
        graph_node = factory.make_graph_session_info()

        expires = graph_node.get_expires_at()
        issued_at = graph_node.get_issued_at()

        self.assertIsInstance(expires, datetime)
        self.assertIsInstance(issued_at, datetime)
