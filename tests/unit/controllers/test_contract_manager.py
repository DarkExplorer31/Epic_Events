"""Unit test for Contract manager"""

import unittest
from unittest.mock import MagicMock, patch

from models.contractmodel import ContractModel
from models.clientmodel import ClientModel
from views.contractview import ContractView
from controllers.contractmanager import ContractManager


class TestContractManager(unittest.TestCase):
    def setUp(self):
        self.mocked_session = MagicMock()
        self.mocked_user_authenticate = MagicMock()
        self.contract_manager = ContractManager(
            self.mocked_session, self.mocked_user_authenticate
        )
        self.contract_view = MagicMock()
        self.contract_model = MagicMock()
        self.client_model = MagicMock()

    @patch.object(ContractModel, "get_all")
    def test_get_all_contracts(self, mocked_get_all):
        mocked_contracts = [
            {"id": 1, "name": "Contract 1"},
            {"id": 2, "name": "Contract 2"},
        ]
        mocked_get_all.return_value = mocked_contracts
        returned_contracts = self.contract_manager.get_all_contracts()
        self.assertEqual(returned_contracts, mocked_contracts)

    @patch.object(ClientModel, "get_all")
    @patch.object(ClientModel, "get_all_by_user_responsibility")
    def test_get_all_clients_under_responsibility_manager(
        self, mocked_get_all_by_user_responsibility, mocked_get_all
    ):
        mocked_clients = [{"id": 1, "name": "Client 1"}, {"id": 2, "name": "Client 2"}]
        self.contract_manager.role = "Manager"
        mocked_get_all.return_value = mocked_clients
        returned_clients = self.contract_manager.get_all_clients_under_responsibility()
        self.assertEqual(returned_clients, mocked_clients)

    @patch.object(ClientModel, "get_all_by_user_responsibility")
    def test_get_all_clients_under_responsibility_sales(
        self, mocked_get_all_by_user_responsibility
    ):
        mocked_clients = [{"id": 1, "name": "Client 1"}, {"id": 2, "name": "Client 2"}]
        self.contract_manager.role = "Sales"
        mocked_get_all_by_user_responsibility.return_value = mocked_clients
        returned_clients = self.contract_manager.get_all_clients_under_responsibility()
        self.assertEqual(returned_clients, mocked_clients)

    @patch.object(ContractView, "ask_status")
    @patch.object(ContractModel, "get_all_by_status")
    def test_get_all_contracts_by_filter(
        self, mocked_get_all_by_status, mocked_ask_status
    ):
        mocked_status = "Active"
        mocked_ask_status.return_value = mocked_status
        mocked_contracts = [
            {"id": 1, "name": "Contract 1", "status": "Active"},
            {"id": 2, "name": "Contract 2", "status": "Active"},
        ]
        mocked_get_all_by_status.return_value = mocked_contracts
        self.contract_manager.get_all_contracts_by_filter()
        mocked_ask_status.assert_called_once()

    @patch.object(ContractModel, "search")
    @patch.object(ContractView, "search_contract")
    @patch.object(ContractManager, "get_all_contracts")
    def test_select_contract(
        self, mocked_get_all_contracts, mocked_search_contract, mocked_search
    ):
        mocked_contract = {"id": 1, "name": "Contract 1"}
        mocked_get_all_contracts.return_value = [mocked_contract]
        mocked_search_contract.return_value = 1
        mocked_search.return_value = mocked_contract
        selected_contract = self.contract_manager.select_contract()
        self.contract_view.display_unfound_contract.assert_not_called()
        self.assertEqual(selected_contract, mocked_contract)

    @patch.object(ClientModel, "search")
    @patch.object(ContractView, "search_client_under_responsibility")
    @patch.object(ContractManager, "get_all_clients_under_responsibility")
    def test_select_client_under_responsibility(
        self,
        mocked_get_all_clients_under_responsibility,
        mocked_search_client_under_responsibility,
        mocked_search,
    ):
        mocked_client = {"id": 1, "name": "Client 1"}
        mocked_get_all_clients_under_responsibility.return_value = [mocked_client]
        mocked_search_client_under_responsibility.return_value = "john@example.com"
        mocked_search.return_value = mocked_client
        self.contract_manager.role = "Manager"
        selected_client = self.contract_manager.select_client_under_responsibility()
        self.contract_view.display_client_is_not_under_responsibility.assert_not_called()
        self.contract_view.display_unfound_client.assert_not_called()
        self.assertEqual(selected_client, mocked_client)

    @patch.object(ContractManager, "select_contract")
    @patch.object(ContractModel, "update")
    @patch.object(ContractView, "get_update_contract_informations")
    @patch.object(ContractView, "display_contract_is_update")
    @patch.object(ContractView, "display_contract_is_not_update")
    @patch.object(ContractView, "display_contract_is_not_under_responsibility")
    def test_update_contract(
        self,
        mocked_display_not_under_responsibility,
        mocked_display_not_update,
        mocked_display_update,
        mocked_get_update_contract_informations,
        mocked_update,
        mocked_select_contract,
    ):
        mocked_contract = {
            "id": 1,
            "name": "Contract 1",
            "user_id": self.mocked_user_authenticate.id,
        }
        mocked_get_update_contract_informations.return_value = mocked_contract
        mocked_select_contract.return_value = mocked_contract
        mocked_update.return_value = True
        self.contract_manager.role = "Manager"
        self.contract_manager.update_contract()
        mocked_select_contract.assert_called_once()
        mocked_get_update_contract_informations.assert_called_once_with(mocked_contract)
        mocked_update.assert_called_once_with(mocked_contract)
        mocked_display_update.assert_called_once()
        mocked_display_not_under_responsibility.assert_not_called()
        mocked_display_not_update.assert_not_called()

    @patch.object(ContractManager, "select_contract")
    @patch.object(ContractModel, "delete")
    @patch.object(ContractView, "display_contract_is_delete")
    @patch.object(ContractView, "display_contract_is_not_delete")
    def test_delete_contract(
        self,
        mocked_display_contract_is_not_delete,
        mocked_display_contract_is_delete,
        mocked_delete,
        mocked_select_contract,
    ):
        mocked_contract = {"id": 1, "name": "Contract 1"}
        mocked_select_contract.return_value = mocked_contract
        mocked_delete.return_value = True
        self.contract_manager.delete_contract()
        mocked_select_contract.assert_called_once()
        mocked_delete.assert_called_once_with(mocked_contract)
        mocked_display_contract_is_delete.assert_called_once()
        mocked_display_contract_is_not_delete.assert_not_called()

    @patch.object(ContractView, "choice_menu")
    @patch.object(ContractManager, "get_all_contracts")
    def test_menu_show_all_contracts(
        self, mocked_get_all_contracts, mocked_choice_menu
    ):
        mocked_choice_menu.return_value = "t"
        self.contract_manager.menu()
        mocked_get_all_contracts.assert_called_once()

    @patch.object(ContractView, "choice_menu")
    @patch.object(ContractManager, "get_all_contracts_by_filter")
    def test_menu_show_all_contracts_by_filter_for_sales(
        self, mocked_get_all_contracts_by_filter, mocked_choice_menu
    ):
        mocked_choice_menu.return_value = "tf"
        self.contract_manager.role = "Sales"
        self.contract_manager.menu()
        mocked_get_all_contracts_by_filter.assert_called_once()

    @patch.object(ContractView, "choice_menu")
    @patch.object(ContractManager, "create_new_contract")
    def test_menu_create_new_contract_for_manager(
        self, mocked_create_new_contract, mocked_choice_menu
    ):
        mocked_choice_menu.return_value = "a"
        self.contract_manager.role = "Manager"
        self.contract_manager.menu()
        mocked_create_new_contract.assert_called_once()

    @patch.object(ContractView, "choice_menu")
    @patch.object(ContractManager, "delete_contract")
    def test_menu_delete_contract_for_manager(
        self, mocked_delete_contract, mocked_choice_menu
    ):
        mocked_choice_menu.return_value = "d"
        self.contract_manager.role = "Manager"
        self.contract_manager.menu()
        mocked_delete_contract.assert_called_once()

    @patch.object(ContractView, "choice_menu")
    @patch.object(ContractView, "display_not_authorized")
    def test_menu_display_not_authorized(
        self, mocked_display_not_authorized, mocked_choice_menu
    ):
        mocked_choice_menu.return_value = "other"
        self.contract_manager.menu()
        mocked_display_not_authorized.assert_called_once()


if __name__ == "__main__":
    unittest.main()
