"""Unit test for Contract view"""

import unittest
from unittest.mock import patch, MagicMock

from models.db_models import StatusEnum
from views.contractview import ContractView


class TestContractView(unittest.TestCase):

    def setUp(self):
        self.contract_view = ContractView()

    # Display methods tests
    @patch("views.contractview.display_green_message")
    def test_display_contracts_with_contracts(self, mocked_green_message):
        contracts = ["Contract 1", "Contract 2"]
        self.contract_view.display_contracts(contracts)
        mocked_green_message.assert_called_once_with(
            "Voici la liste des contracts actuels:\n"
        )

    @patch("views.contractview.display_red_message")
    def test_display_contracts_without_contracts(self, mocked_red_message):
        contracts = []
        self.contract_view.display_contracts(contracts)
        mocked_red_message.assert_called_once_with(
            "Votre liste de contrat actuel est vide.\n"
        )

    @patch("views.contractview.display_green_message")
    def test_display_clients_under_responsibility_with_clients(
        self, mocked_green_message
    ):
        clients = ["Client 1", "Client 2"]
        self.contract_view.display_clients_under_responsibility(clients)
        mocked_green_message.assert_called_once_with(
            "Voici la liste des clients qui sont sous votre responsabilité:\n"
        )

    @patch("views.contractview.display_red_message")
    def test_display_clients_under_responsibility_without_clients(
        self, mocked_red_message
    ):
        clients = []
        self.contract_view.display_clients_under_responsibility(clients)
        mocked_red_message.assert_called_once_with(
            "Vous n'avez pas de clients sous votre responsabilité,"
            + " vous devez en créer au moins un afin de poursuivre.\n"
        )

    @patch("views.contractview.display_red_message")
    def test_display_client_is_not_under_responsibility(
        self, mocked_display_red_message
    ):
        self.contract_view.display_client_is_not_under_responsibility()
        mocked_display_red_message.assert_called_with(
            "Le client n'est pas sous votre responsabilité."
        )

    @patch("views.contractview.display_red_message")
    def test_display_unfound_client(self, mocked_display_red_message):
        self.contract_view.display_unfound_client()
        mocked_display_red_message.assert_called_with("Le client n'a pas été trouvé.")

    @patch("views.contractview.display_green_message")
    def test_display_created(self, mocked_display_green_message):
        self.contract_view.display_created()
        mocked_display_green_message.assert_called_with("Le contrat a été créé.")

    @patch("views.contractview.display_red_message")
    def test_display_not_created(self, mocked_display_red_message):
        self.contract_view.display_not_created()
        mocked_display_red_message.assert_called_once()

    @patch("views.contractview.display_red_message")
    def test_display_unfound_contract(self, mocked_display_red_message):
        self.contract_view.display_unfound_contract()
        mocked_display_red_message.assert_called_once()

    @patch("views.contractview.display_red_message")
    def test_display_contract_is_not_under_responsibility(
        self, mocked_display_red_message
    ):
        self.contract_view.display_contract_is_not_under_responsibility()
        mocked_display_red_message.assert_called_once()

    @patch("views.contractview.display_green_message")
    def test_display_contract_is_update(self, mocked_display_green_message):
        self.contract_view.display_contract_is_update()
        mocked_display_green_message.assert_called_once()

    @patch("views.contractview.display_red_message")
    def test_display_contract_is_not_update(self, mocked_display_red_message):
        self.contract_view.display_contract_is_not_update()
        mocked_display_red_message.assert_called_once()

    @patch("views.contractview.display_green_message")
    def test_display_contract_is_delete(self, mocked_display_green_message):
        self.contract_view.display_contract_is_delete()
        mocked_display_green_message.assert_called_with("Le contrat a été supprimé.")

    @patch("views.contractview.display_red_message")
    def test_display_contract_is_not_delete(self, mocked_display_red_message):
        self.contract_view.display_contract_is_not_delete()
        mocked_display_red_message.assert_called_with(
            "Le contrat n'a pas été supprimé."
        )

    @patch("views.contractview.display_red_message")
    def test_display_not_authorized(self, mocked_display_red_message):
        self.contract_view.display_not_authorized()
        mocked_display_red_message.assert_called_once()

    # Searching methods tests
    @patch("views.contractview.Menu.information_menu")
    def test_search_client_under_responsibility(self, mock_information_menu):
        mock_information_menu.return_value = "john@example.com"
        email = self.contract_view.search_client_under_responsibility()
        self.assertEqual(email, "john@example.com")

    @patch("views.contractview.Menu.information_menu")
    def test_search_contract_with_valid_id(self, mock_information_menu):
        mock_information_menu.return_value = "1"
        contract_id = self.contract_view.search_contract()
        self.assertEqual(contract_id, 1)

    @patch("views.contractview.Menu.information_menu")
    def test_search_contract_with_invalid_id(self, mock_information_menu):
        mock_information_menu.return_value = "abc"
        contract_id = self.contract_view.search_contract()
        self.assertIsNone(contract_id)

    # Other methods
    @patch("views.contractview.Menu.information_menu")
    def test_ask_status_with_valid_status(self, mock_information_menu):
        mock_information_menu.return_value = "Non signé"
        status = self.contract_view.ask_status()
        self.assertEqual(status, StatusEnum.UNSIGNED)

    @patch("views.contractview.Menu.information_menu")
    def test_ask_status_with_invalid_status(self, mock_information_menu):
        mock_information_menu.return_value = "Unvalid"
        status = self.contract_view.ask_status()
        self.assertIsNone(status)

    @patch("views.contractview.Menu.information_menu")
    def test_get_new_contract_information_with_valid_input(self, mock_information_menu):
        mock_information_menu.side_effect = ["1000", "Pas payé", "500"]
        contract_info = self.contract_view.get_new_contract_information()
        self.assertEqual(contract_info["total_cost"], 1000)
        self.assertEqual(contract_info["balance"], 500)
        self.assertEqual(contract_info["status"], StatusEnum.UNPAID)

    @patch("views.contractview.Menu.information_menu")
    def test_get_update_contract_informations_status_unchanged(
        self, mock_information_menu
    ):
        contract = MagicMock()
        contract.status = StatusEnum.UNSIGNED
        mock_information_menu.side_effect = ["Non signé"]
        updated_contract = self.contract_view.get_update_contract_informations(contract)
        self.assertEqual(updated_contract.status, StatusEnum.UNSIGNED)

    @patch("views.contractview.Menu.information_menu")
    @patch("views.contractview.display_red_message")
    def test_get_update_contract_informations_status_changed(
        self, mock_display_red_message, mock_information_menu
    ):
        contract = MagicMock()
        contract.status = "Non signé"
        mock_information_menu.side_effect = ["Payé"]
        updated_contract = self.contract_view.get_update_contract_informations(contract)
        self.assertEqual(updated_contract.status, StatusEnum.PAID)
        self.assertEqual(updated_contract.balance, 0.0)
        self.assertFalse(mock_display_red_message.called)

    @patch("views.contractview.Menu.crud_menu")
    @patch("views.contractview.Menu.no_permission_menu")
    def test_choice_contrat_menu_manager(self, mock_no_permission_menu, mock_crud_menu):
        user_role = "Manager"
        mock_crud_menu.return_value = "crud_menu_output"
        choice = self.contract_view.choice_menu(user_role)
        self.assertEqual(choice, "crud_menu_output")
        mock_crud_menu.assert_called_once_with("contrat")
        mock_no_permission_menu.assert_not_called()

    @patch("views.contractview.Menu.global_menu")
    @patch("views.contractview.Menu.no_permission_menu")
    def test_choice_contrat_menu_sales(self, mock_no_permission_menu, mock_global_menu):
        user_role = "Sales"
        mock_global_menu.return_value = "global_menu_output"
        choice = self.contract_view.choice_menu(user_role)
        self.assertEqual(choice, "global_menu_output")
        mock_global_menu.assert_called_once_with(
            {
                "t": "Voir tout les contrats",
                "tf": "Voir les contrats filtrés par status",
                "u": "Mettre à jour le contrat d'un de vos client",
            }
        )
        mock_no_permission_menu.assert_not_called()

    @patch("views.contractview.Menu.no_permission_menu")
    def test_choice_contrat_menu_no_permission(self, mock_no_permission_menu):
        user_role = "Other"
        mock_no_permission_menu.return_value = "no_permission_menu_output"
        choice = self.contract_view.choice_menu(user_role)
        self.assertEqual(choice, "no_permission_menu_output")
        mock_no_permission_menu.assert_called_once_with("contrat")
