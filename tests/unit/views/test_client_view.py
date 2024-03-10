"""Unit test for Client view"""

import unittest
from unittest.mock import patch, call, MagicMock
from views.clientview import ClientView


class TestClientView(unittest.TestCase):
    def setUp(self):
        self.client_view = ClientView()

    # Display methods tests
    @patch("builtins.print")
    def test_display_clients_with_clients(self, mocked_print):
        clients = ["Client 1", "Client 2"]
        expected_calls = [call("-Client 1"), call("-Client 2")]
        self.client_view.display_clients(clients)
        mocked_print.assert_has_calls(expected_calls)

    @patch("views.clientview.display_red_message")
    def test_display_clients_empty(self, mocked_display_red_message):
        clients = []
        self.client_view.display_clients(clients)
        mocked_display_red_message.assert_called_with(
            "Votre liste de client actuel est vide.\n"
        )

    @patch("views.clientview.display_green_message")
    def test_display_created(self, mocked_display_green_message):
        self.client_view.display_created()
        mocked_display_green_message.assert_called_with("Le client a été créé.")

    @patch("views.clientview.display_red_message")
    def test_display_not_created(self, mocked_display_red_message):
        self.client_view.display_not_created()
        mocked_display_red_message.assert_called_once()

    @patch("views.clientview.display_red_message")
    def test_display_unfound_client(self, mocked_display_red_message):
        self.client_view.display_unfound_client()
        mocked_display_red_message.assert_called_with("Le client n'a pas été trouvé.")

    @patch("views.clientview.display_red_message")
    def test_display_client_is_not_under_responsibility(
        self, mocked_display_red_message
    ):
        self.client_view.display_client_is_not_under_responsibility()
        mocked_display_red_message.assert_called_with(
            "Le client n'est pas sous votre responsabilité."
        )

    @patch("views.clientview.display_green_message")
    def test_display_client_is_update(self, mocked_display_green_message):
        self.client_view.display_client_is_update()
        mocked_display_green_message.assert_called_with("Le client a été mis à jour.")

    @patch("views.clientview.display_red_message")
    def test_display_client_is_not_update(self, mocked_display_red_message):
        self.client_view.display_client_is_not_update()
        mocked_display_red_message.assert_called()

    @patch("views.clientview.display_green_message")
    def test_display_client_is_delete(self, mocked_display_green_message):
        self.client_view.display_client_is_delete()
        mocked_display_green_message.assert_called_with("Le client a été supprimé.")

    @patch("views.clientview.display_red_message")
    def test_display_client_is_not_delete(self, mocked_display_red_message):
        self.client_view.display_client_is_not_delete()
        mocked_display_red_message.assert_called_with("Le client n'a pas été supprimé.")

    @patch("views.clientview.display_red_message")
    def test_display_not_authorized(self, mocked_display_red_message):
        self.client_view.display_not_authorized()
        mocked_display_red_message.assert_called()

    # Other methods
    @patch("builtins.input")
    def test_get_new_client_information(self, mock_input):
        mock_input.side_effect = [
            "John Doe",
            "john@example.com",
            "123456789",
            "ABC Inc.",
        ]
        expected_result = {
            "complete_name": "John Doe",
            "email": "john@example.com",
            "phone_number": "123456789",
            "company_name": "ABC Inc.",
        }
        result = self.client_view.get_new_client_information()
        self.assertEqual(result, expected_result)

    @patch("builtins.input")
    def test_get_new_client_information_should_return_None(self, mocked_input):
        mocked_input.side_effect = [
            "John Doe",
            "q",
        ]
        result = self.client_view.get_new_client_information()
        expected_result = None
        self.assertEqual(result, expected_result)

    @patch("builtins.input")
    def test_search_client_should_return_email(self, mocked_input):
        mocked_input.return_value = "john@example.com"
        result = self.client_view.search_client()
        expected_result = "john@example.com"
        self.assertEqual(result, expected_result)

    @patch("views.clientview.Menu.information_menu")
    def test_get_update_client_informations_should_return_updated_client(
        self,
        mocked_information_menu,
    ):
        mocked_client = MagicMock()
        mocked_client.complete_name = "John Doe"
        mocked_client.email = "john@example.com"
        mocked_client.phone_number = "123456789"
        mocked_client.company_name = "ABC Inc."
        mocked_information_menu.side_effect = [
            "Jane Smith",
            "jane@example.com",
            "987654321",
            "XYZ Corp",
        ]
        result = self.client_view.get_update_client_informations(mocked_client)
        self.assertEqual(result.complete_name, "Jane Smith")
        self.assertEqual(result.email, "jane@example.com")
        self.assertEqual(result.phone_number, "987654321")
        self.assertEqual(result.company_name, "XYZ Corp")


if __name__ == "__main__":
    unittest.main()
