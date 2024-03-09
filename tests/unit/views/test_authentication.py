"""Unit test for Authentication view"""

import unittest
from unittest.mock import patch, MagicMock
from views.authenticationview import AuthenticationView
from utils import Menu


class TestAuthenticationView(unittest.TestCase):

    def setUp(self):
        self.auth_view = AuthenticationView()

    @patch("views.authenticationview.display_red_message")
    def test_display_quit(self, mocked_display_red_message):
        self.auth_view.display_quit()
        mocked_display_red_message.assert_called_once_with("Vous quittez le programme.")

    @patch("views.authenticationview.display_red_message")
    def test_display_acces_non_autorise(self, mocked_display_red_message):
        self.auth_view.display_acces_non_autorise()
        mocked_display_red_message.assert_called_once_with(
            "Les identifiants fournis sont incorrects.\nAccès non autorisé"
        )

    @patch("views.authenticationview.display_green_message")
    def test_display_acces_autorise(self, mocked_display_green_message):
        self.auth_view.display_acces_autorise()
        mocked_display_green_message.assert_called_once_with("Accès autorisé")

    @patch("views.authenticationview.display_green_message")
    def test_display_password_changed(self, mocked_display_green_message):
        self.auth_view.display_password_changed()
        mocked_display_green_message.assert_called_once_with(
            "Mot de passe changé.\nAccès autorisé"
        )

    @patch("views.authenticationview.display_green_message")
    def test_display_hello_user(self, mocked_display_green_message):
        user = MagicMock(complete_name="John Doe")
        self.auth_view.display_hello_user(user)
        mocked_display_green_message.assert_called_once_with("Bonjour, John Doe")

    @patch("builtins.input", return_value="JohnDoe")
    def test_ask_authentication(self, mocked_input):
        with patch("getpass.getpass", return_value="password"):
            credentials = self.auth_view.ask_authentication()
        self.assertEqual(credentials, {"login": "JohnDoe", "password": "password"})

    @patch("getpass.getpass", return_value="password")
    def test_add_new_password(self, mocked_getpass):
        new_password = self.auth_view.add_new_password("oldpassword")
        self.assertEqual(new_password, "password")

    @patch("getpass.getpass", side_effect=["short", "password", "password"])
    def test_add_new_password_short_password(self, mocked_getpass):
        new_password = self.auth_view.add_new_password("oldpassword")
        self.assertEqual(new_password, "password")

    @patch(
        "getpass.getpass",
        side_effect=["password", "wrongpassword", "password", "password"],
    )
    @patch("views.authenticationview.display_red_message")
    def test_add_new_password_wrong_confirmation(self, mocked_display, mocked_getpass):
        new_password = self.auth_view.add_new_password("oldpassword")
        mocked_display.assert_called_with("Votre mot de passe ne correspond pas")

    def test_select_menu_by_role_sales(self):
        user_mock = MagicMock()
        user_mock.role.value = "Sales"
        with patch(
            "utils.Menu.global_menu",
            return_value="c",
        ):
            choice = self.auth_view.select_menu_by_role(user_mock)
        self.assertEqual(choice, "c")

    def test_select_menu_by_role_manager(self):
        user_mock = MagicMock()
        user_mock.role.value = "Manager"
        with patch(
            "utils.Menu.global_menu",
            return_value="u",
        ):
            choice = self.auth_view.select_menu_by_role(user_mock)
        self.assertEqual(choice, "u")

    def test_select_menu_by_role_support(self):
        user_mock = MagicMock()
        user_mock.role.value = "Support"
        with patch(
            "utils.Menu.global_menu",
            return_value="e",
        ):
            choice = self.auth_view.select_menu_by_role(user_mock)
        self.assertEqual(choice, "e")

    def test_select_menu_by_role_invalid_choice(self):
        user_mock = MagicMock()
        user_mock.role.value = "UnknownRole"
        with patch(
            "utils.Menu.global_menu",
            return_value="x",
        ):
            choice = self.auth_view.select_menu_by_role(user_mock)
        self.assertIsNone(choice)


if __name__ == "__main__":
    unittest.main()
