"""Unit test for Client manager"""

import unittest
from unittest.mock import MagicMock, patch

from models.clientmodel import ClientModel
from views.clientview import ClientView
from controllers.clientmanager import ClientManager


class TestClientManager(unittest.TestCase):
    def setUp(self):
        self.mocked_session = MagicMock()
        self.mocked_user_authenticate = MagicMock()
        self.client_manager = ClientManager(
            self.mocked_session, self.mocked_user_authenticate
        )
        self.client_view = ClientView()
        self.client_model = ClientModel(self.mocked_session)
