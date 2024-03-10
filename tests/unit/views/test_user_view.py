"""Unit test for User view"""

import unittest
from unittest.mock import patch, call, Mock, MagicMock
from views.userview import UserView


class TestUserView(unittest.TestCase):
    def setUp(self):
        self.user_view = UserView()

    # Display functions tests
    def test_display_users(self):
        users = ["user1", "user2", "user3"]
        expected_calls = [call("-user1"), call("-user2"), call("-user3")]
        with patch("builtins.print") as mocked_print:
            self.user_view.display_users(users)
            mocked_print.assert_has_calls(expected_calls)

    def test_display_roles(self):
        expected_output = [
            call("Les roles qui peuvent être: "),
            call("-Sales"),
            call("-Manager"),
            call("-Support"),
            call("\n"),
        ]
        with patch("builtins.print") as mocked_print:
            self.user_view.display_roles()
            mocked_print.assert_has_calls(expected_output)

    @patch("views.userview.display_green_message")
    def test_display_created_user(self, mocked_display_green_message):
        self.user_view.display_created()
        mocked_display_green_message.assert_called_once_with(
            "L'utilisateur a été créé."
        )

    @patch("views.userview.display_red_message")
    def test_display_not_created(self, mocked_display_red_message):
        self.user_view.display_not_created()
        mocked_display_red_message.assert_called_once_with(
            "L'utilisateur n'a pas été créé."
        )

    @patch("views.userview.display_red_message")
    def test_display_unfound_user(self, mocked_display_red_message):
        self.user_view.display_unfound_user()
        mocked_display_red_message.assert_called_once_with(
            "L'utilisateur n'a pas été trouvé."
        )

    def test_display_selected_user(self):
        user = Mock()
        user.email = "john@example.com"
        user.role = "Sales"
        user.phone_number = "123456789"
        user.complete_name = "John Doe"
        expected_output = (
            f"Vous avez sélectionné l'utilisateur : {user.email}."
            + "\nVous ne pourrez changer que le rôle, le nom complet"
            + " ou le numéro de téléphone.\n"
            + f" Actuellement, son rôle est : {user.role}.\n"
            + f"Le numéro de téléphone est : {user.phone_number}.\n"
            + f"Et le nom complet : {user.complete_name}.\n\n"
        )
        with patch("builtins.print") as mocked_print:
            self.user_view.display_selected_user(user)
            mocked_print.assert_called_once_with(expected_output)

    @patch("views.userview.display_green_message")
    def test_display_user_is_update(self, mocked_display_green_message):
        self.user_view.display_user_is_update()
        mocked_display_green_message.assert_called_once()

    @patch("views.userview.display_red_message")
    def test_display_user_is_not_update(self, mocked_display_red_message):
        self.user_view.display_user_is_not_update()
        mocked_display_red_message.assert_called_once()

    @patch("views.userview.display_green_message")
    def test_display_user_is_delete(self, mocked_display_green_message):
        self.user_view.display_user_is_delete()
        mocked_display_green_message.assert_called_once()

    @patch("views.userview.display_red_message")
    def test_display_user_is_not_delete(self, mocked_display_red_message):
        self.user_view.display_user_is_not_delete()
        mocked_display_red_message.assert_called_once()

    @patch("views.userview.display_red_message")
    def test_display_user_is_not_authorized(self, mocked_display_red_message):
        self.user_view.display_user_is_not_authorized()
        mocked_display_red_message.assert_called_once()

    # Other methods
    @patch("views.userview.generate_password")
    @patch("builtins.input")
    def test_get_new_user_information(self, mocked_input, mocked_generate_password):
        mocked_input.side_effect = [
            "Sales",
            "John Doe",
            "john@example.com",
            "123456789",
        ]
        mocked_generate_password.return_value = "mocked_password"
        result = self.user_view.get_new_user_information()
        expected_result = {
            "role": "Sales",
            "complete_name": "John Doe",
            "email": "john@example.com",
            "phone_number": "123456789",
            "password": "mocked_password",
        }
        self.assertEqual(result, expected_result)

    @patch("views.userview.generate_password")
    @patch("builtins.input")
    def test_get_new_user_information_should_return_None(
        self, mocked_input, mocked_generate_password
    ):
        mocked_input.side_effect = [
            "Sales",
            "q",
        ]
        mocked_generate_password.return_value = None
        result = self.user_view.get_new_user_information()
        expected_result = None
        self.assertEqual(result, expected_result)

    @patch("builtins.input")
    def test_search_user_should_return_email(self, mocked_input):
        mocked_input.return_value = "john@example.com"
        result = self.user_view.search_user()
        expected_result = "john@example.com"
        self.assertEqual(result, expected_result)

    @patch("views.userview.display_green_message")
    @patch("views.userview.display_red_message")
    @patch("views.userview.Menu.information_menu")
    def test_get_update_user_informations_should_return_updated_user(
        self,
        mocked_information_menu,
        mocked_red_message,
        mocked_green_message,
    ):
        mocked_user = MagicMock()
        mocked_user.role = "Sales"
        mocked_user.complete_name = "John Doe"
        mocked_user.phone_number = "123456789"
        mocked_information_menu.side_effect = ["Manager", "Updated Name", "987654321"]
        result = self.user_view.get_update_user_informations(mocked_user)
        self.assertEqual(result.role, "MANAGER")
        self.assertEqual(result.complete_name, "Updated Name")
        self.assertEqual(result.phone_number, "987654321")
        mocked_red_message.assert_not_called()
        mocked_green_message.assert_called()

    @patch("views.userview.Menu.crud_menu")
    def test_choice_menu_should_return_user_choice(self, mocked_crud_menu):
        mocked_crud_menu.return_value = "Ajoutez un utilisateur"
        result = self.user_view.choice_menu()
        self.assertEqual(result, "Ajoutez un utilisateur")


if __name__ == "__main__":
    unittest.main()
