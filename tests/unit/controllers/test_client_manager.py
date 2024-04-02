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

    @patch.object(ClientView, "get_new_client_information")
    @patch.object(ClientModel, "create")
    @patch.object(ClientView, "display_created")
    @patch.object(ClientView, "display_not_created")
    def test_create_new_client(
        self,
        mocked_display_not_created,
        mocked_display_created,
        mocked_create,
        mocked_get_new_client_information,
    ):
        mocked_get_new_client_information.return_value = {
            "complete_name": "John Doe",
            "email": "john@example.com",
            "phone_number": "123456789",
            "company_name": "ABC Inc.",
        }
        mocked_create.return_value = True
        self.client_manager.create_new_client()
        mocked_create.assert_called_once_with(
            user_id=self.mocked_user_authenticate.id,
            complete_name="John Doe",
            email="john@example.com",
            phone_number="123456789",
            company_name="ABC Inc.",
        )
        mocked_display_created.assert_called_once()
        mocked_display_not_created.assert_not_called()

    @patch.object(ClientView, "search_client")
    @patch.object(ClientModel, "search")
    @patch.object(ClientView, "display_unfound_client")
    def test_select_client(
        self, mocked_display_unfound_client, mocked_search, mocked_search_client
    ):
        mocked_search_client.return_value = "john@example.com"
        mocked_search.return_value = {"id": 1, "name": "John Doe"}
        result = self.client_manager.select_client()
        mocked_search.assert_called_once_with(email="john@example.com")
        mocked_display_unfound_client.assert_not_called()
        self.assertEqual(result, {"id": 1, "name": "John Doe"})

    @patch.object(ClientManager, "select_client")
    @patch.object(ClientModel, "update")
    @patch.object(ClientView, "display_client_is_update")
    @patch.object(ClientView, "display_client_is_not_update")
    @patch.object(ClientView, "get_update_client_informations")
    def test_update_client(
        self,
        mocked_get_update_client_informations,
        mocked_display_client_is_not_update,
        mocked_display_client_is_update,
        mocked_update,
        mocked_select_client,
    ):
        mocked_select_client.return_value = MagicMock(
            user_id=self.mocked_user_authenticate.id
        )
        mocked_get_update_client_informations.return_value = {
            "complete_name": "John Doe",
            "email": "john@example.com",
            "phone_number": "123456789",
            "company_name": "ABC Inc.",
        }
        mocked_update.return_value = True
        self.client_manager.update_client()
        mocked_select_client.assert_called_once()
        mocked_get_update_client_informations.assert_called_once()
        mocked_update.assert_called_once_with(
            {
                "complete_name": "John Doe",
                "email": "john@example.com",
                "phone_number": "123456789",
                "company_name": "ABC Inc.",
            }
        )
        mocked_display_client_is_update.assert_called_once()
        mocked_display_client_is_not_update.assert_not_called()

    @patch.object(ClientManager, "select_client")
    @patch.object(ClientModel, "delete")
    @patch.object(ClientView, "display_client_is_delete")
    @patch.object(ClientView, "display_client_is_not_delete")
    def test_delete_client(
        self,
        mocked_display_client_is_not_delete,
        mocked_display_client_is_delete,
        mocked_delete,
        mocked_select_client,
    ):
        mocked_select_client.return_value = MagicMock(
            user_id=self.mocked_user_authenticate.id
        )
        mocked_delete.return_value = True
        self.client_manager.delete_client()
        mocked_select_client.assert_called_once()
        mocked_delete.assert_called_once_with(mocked_select_client.return_value)
        mocked_display_client_is_delete.assert_called_once()
        mocked_display_client_is_not_delete.assert_not_called()

    @patch.object(ClientView, "choice_menu")
    def test_menu_get_all_clients(self, mocked_choice_menu):
        mocked_choice_menu.return_value = "t"
        self.client_manager.role = "Sales"
        with patch.object(ClientManager, "get_all_clients") as mocked_get_all_clients:
            self.client_manager.menu()
            mocked_get_all_clients.assert_called_once()

    @patch.object(ClientView, "choice_menu")
    def test_menu_create_new_client_authorized(self, mocked_choice_menu):
        mocked_choice_menu.return_value = "a"
        self.client_manager.role = "Sales"
        with patch.object(
            ClientManager, "create_new_client"
        ) as mocked_create_new_client:
            self.client_manager.menu()
            mocked_create_new_client.assert_called_once()

    @patch.object(ClientView, "choice_menu")
    def test_menu_create_new_client_unauthorized(self, mocked_choice_menu):
        mocked_choice_menu.return_value = "a"
        self.client_manager.role = "SomeRole"
        with patch.object(
            ClientView, "display_not_authorized"
        ) as mocked_display_not_authorized:
            self.client_manager.menu()
            mocked_display_not_authorized.assert_called_once()

    @patch.object(ClientView, "choice_menu")
    def test_menu_delete_client_authorized(self, mocked_choice_menu):
        mocked_choice_menu.return_value = "d"
        self.client_manager.role = "Sales"
        with patch.object(ClientManager, "delete_client") as mocked_delete_client:
            self.client_manager.menu()
            mocked_delete_client.assert_called_once()

    @patch.object(ClientView, "choice_menu")
    def test_menu_delete_client_unauthorized(self, mocked_choice_menu):
        mocked_choice_menu.return_value = "d"
        self.client_manager.role = "SomeRole"
        with patch.object(
            ClientView, "display_not_authorized"
        ) as mocked_display_not_authorized:
            self.client_manager.menu()
            mocked_display_not_authorized.assert_called_once()
